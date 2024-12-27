import zlib
import base64

import gzip
import base64


def compress_string(input_string):
    # Decode the Base64 string
    decoded_data = base64.b64decode(input_string)

    # Compress the data using gzip
    compressed_data = gzip.compress(decoded_data)

    # Encode the compressed data back to Base64
    compressed_base64 = base64.b64encode(compressed_data).decode('utf-8')

    return compressed_base64