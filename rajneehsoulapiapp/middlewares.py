import os
import json
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from django.http import JsonResponse, HttpResponse
from django.conf import settings


def _get_encryption_key():
    # Ensure the key is fetched from settings or environment variables
    key = getattr(settings, "ENCRYPTION_KEY", None)
    if not key:
        raise ValueError("ENCRYPTION_KEY is not set in settings.")
    # Ensure the key is 32 bytes (AES-256)
    return key.ljust(32, '0')[:32].encode()


class EncryptResponseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.key = _get_encryption_key()
        # Optionally define the list of paths where encryption is enabled
        self.encryption_disabled_paths = getattr(settings, "ENCRYPTION_DISABLED_PATHS", [])

    def encrypt_data(self, data):
        print("Data to encrypt: ", data)  # Debug original data
        try:
            # Convert data to JSON string if it's not already a string
            if isinstance(data, bytes):  # Decode bytes to string if necessary
                data = data.decode()

            if not isinstance(data, str):  # Serialize other non-string types
                data = json.dumps(data)

            # Generate a random IV (Initialization Vector)
            iv = os.urandom(16)

            # Create the cipher object for AES encryption
            cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=default_backend())

            # Pad the data to make it a multiple of the block size (16 bytes for AES)
            padder = padding.PKCS7(algorithms.AES.block_size).padder()
            padded_data = padder.update(data.encode()) + padder.finalize()

            # Encrypt the data
            encryptor = cipher.encryptor()
            encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

            # Encode the encrypted data and IV in Base64
            encrypted_data_base64 = base64.b64encode(encrypted_data).decode()
            iv_base64 = base64.b64encode(iv).decode()

            print("Encrypted data (base64): ", encrypted_data_base64)  # Debug encrypted data
            print("IV (base64): ", iv_base64)  # Debug IV
            return {"encrypted_data": encrypted_data_base64, "iv": iv_base64}

        except Exception as e:
            print("Encryption error: ", str(e))  # Debug error
            raise RuntimeError(f"Encryption failed: {str(e)}")

    def __call__(self, request):
        print("2" * 100)  # Debug middleware call
        # Get the response from the view
        normalized_path = request.path.rstrip('/')
        print("normalized_path: ", normalized_path)

        # Get the response from the view
        response = self.get_response(request)

        # Check if the normalized path is in the encryption-enabled list
        encryption_disabled = any(
            normalized_path == path.rstrip('/') for path in self.encryption_disabled_paths
        )

        print("encryption_disabled ----> ",encryption_disabled)
        print("response ----> ", response)

        if not encryption_disabled:
            # Skip certain response types like streaming responses
            if hasattr(response, 'streaming') and response.streaming:
                print("Skipping encryption for streaming response.")  # Debug skip reason
                return response

            try:
                # Handle raw content of the response
                content = response.content  # Get raw content
                content_type = response['Content-Type']  # Preserve the original content type
                print("Original Content-Type: ", content_type)  # Debug Content-Type

                # Encrypt the content
                encrypted_response = self.encrypt_data(content)

                # Replace original content with encrypted content
                response.content = json.dumps(encrypted_response).encode()
                response['Content-Type'] = 'application/json'  # Return as JSON
                response['X-Encrypted'] = '1'  # Optional: Header to indicate encryption

            except Exception as e:
                print("Encryption failed: ", str(e))  # Debug encryption failure
                response = JsonResponse({"error": f"Encryption failed: {str(e)}"}, status=500)

        return response
