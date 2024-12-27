import json
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from django.conf import settings
from django.http import JsonResponse


def _get_encryption_key():
    # Ensure the key is fetched from settings or environment variables
    key = getattr(settings, "ENCRYPTION_KEY", None)
    if not key:
        raise ValueError("ENCRYPTION_KEY is not set in settings.")
    # Ensure the key is 32 bytes (AES-256)
    return key.ljust(32, '0')[:32].encode()


class DecryptRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.key = _get_encryption_key()
        self.encryption_disabled_paths = getattr(settings, "ENCRYPTION_DISABLED_PATHS", [])

    def decrypt_data(self, encrypted_data, iv):
        try:
            # Decode the base64-encoded data
            encrypted_data_bytes = base64.b64decode(encrypted_data)
            iv_bytes = base64.b64decode(iv)

            # Create the AES cipher object
            cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv_bytes), backend=default_backend())

            # Decrypt the data
            decryptor = cipher.decryptor()
            padded_data = decryptor.update(encrypted_data_bytes) + decryptor.finalize()

            # Unpad the decrypted data
            unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
            data = unpadder.update(padded_data) + unpadder.finalize()

            # Convert bytes to string
            return data.decode()
        except Exception as e:
            raise ValueError(f"Decryption failed: {str(e)}")

    def __call__(self, request):
        # Normalize path to avoid trailing slash mismatches
        normalized_path = request.path.rstrip('/')
        encryption_disabled = any(
            normalized_path == path.rstrip('/') for path in self.encryption_disabled_paths
        )

        # Skip decryption for disabled paths
        if encryption_disabled:
            return self.get_response(request)

        # Only process POST, PUT, PATCH requests with a body
        if request.method in ["POST", "PUT", "PATCH"]:
            try:
                # Parse JSON from the encrypted request body
                body = json.loads(request.body)

                # Extract encrypted data and IV
                encrypted_data = body.get("encrypted_data")
                iv = body.get("iv")

                if not encrypted_data or not iv:
                    return JsonResponse({"error": "Missing encrypted data or IV"}, status=400)

                # Decrypt the data
                decrypted_data = self.decrypt_data(encrypted_data, iv)

                # Replace request body with decrypted data
                request._body = decrypted_data.encode()
                request.data = json.loads(decrypted_data)  # For DRF compatibility

            except Exception as e:
                return JsonResponse({"error": f"Decryption error: {str(e)}"}, status=400)

        # Continue processing the request
        return self.get_response(request)
