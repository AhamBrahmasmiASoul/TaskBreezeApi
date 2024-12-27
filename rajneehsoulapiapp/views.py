import base64
import json
import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Content
from .serializers import ContentSerializer
from .utils import compress_string  # Import the utility function


@api_view(['POST'])
def encrypt_data(request):
    """
    Encrypt any type of data (string, list, dictionary, etc.) with AES using a given key.
    The data and key are passed in the request body.
    """
    # Extract data and key from the request
    data = request.data.get("data")
    key = request.data.get("key")

    if data is None or key is None:
        return Response({"error": "Both 'data' and 'key' are required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Convert data to JSON string if it's not already a string
        if not isinstance(data, str):
            data = json.dumps(data)  # Serialize non-string data to JSON string

        # Ensure the key is 32 bytes long (for AES-256)
        key = key.ljust(32, '0')[:32].encode()  # Pad or truncate key to 32 bytes

        # Generate a random IV (Initialization Vector)
        iv = os.urandom(16)

        # Create the cipher object for AES encryption
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())

        # Pad the data to make it a multiple of the block size (16 bytes for AES)
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(data.encode()) + padder.finalize()

        # Encrypt the data
        encryptor = cipher.encryptor()
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

        # Encode the encrypted data and IV in Base64
        encrypted_data_base64 = base64.b64encode(encrypted_data).decode()
        iv_base64 = base64.b64encode(iv).decode()

        return Response({
            "encrypted_data": encrypted_data_base64,
            "iv": iv_base64
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def decrypt_data(request):
    """
    Decrypt encrypted data (string, list, dictionary, etc.) with AES using a given key and IV.
    The encrypted_data, key, and IV are passed in the request body.
    """
    # Extract encrypted data, key, and IV from the request
    print("request.data --> ", request.data)
    encrypted_data = request.data.get("encrypted_data")
    key = request.data.get("key")
    iv = request.data.get("iv")

    if encrypted_data is None or key is None or iv is None:
        return Response({
            "error": "All fields 'encrypted_data', 'key', and 'iv' are required."
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Ensure the key is 32 bytes long (for AES-256)
        key = key.ljust(32, '0')[:32].encode()  # Pad or truncate key to 32 bytes

        # Decode the encrypted data and IV from Base64
        encrypted_data = base64.b64decode(encrypted_data)
        iv = base64.b64decode(iv)

        # Create the cipher object for AES decryption
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())

        # Decrypt the data
        decryptor = cipher.decryptor()
        decrypted_padded_data = decryptor.update(encrypted_data) + decryptor.finalize()

        # Remove padding
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()

        # Convert the decrypted data back to its original format (JSON string -> Python object)
        try:
            decrypted_data = json.loads(decrypted_data.decode())
        except json.JSONDecodeError:
            # If it's not JSON, just return it as a string
            decrypted_data = decrypted_data.decode()

        return Response({
            "decrypted_data": decrypted_data
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST'])
def compress_string_view(request):
    """
    API View to compress a string using POST request.
    """
    input_string = request.data.get('input_string')

    if not input_string:
        return Response(
            {"error": "The 'input_string' field is required."},
            status=status.HTTP_400_BAD_REQUEST
        )

    if not isinstance(input_string, str) or not input_string.strip():
        return Response(
            {"error": "The 'input_string' must be a non-empty string."},
            status=status.HTTP_400_BAD_REQUEST
        )

    compressed_output = compress_string(input_string)
    return Response(
        {
            "original_string": input_string,
            "compressed_string": compressed_output,
        },
        status=status.HTTP_200_OK
    )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_content():
    try:
        # Fetch all content records
        content = Content.objects.all()
        # Serialize the data
        serializer = ContentSerializer(content, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)