"""
WHAT IT DOES:
* Uses SHA-256 to return a hexidecimal representation of hased input data

OUTPUTS:
* Within Terminal: The original string of data, followed by the hashed version

AUTHOR: Sophie-Louise Courtney
LAST UPDATED: 27/07/2024
LANGUAGE: Python
"""

import hashlib

def hash_data(data: str) -> str:
    # Create a new sha256 hash object
    sha256_hash = hashlib.sha256()

    # Update the hash object with the bytes of the data
    sha256_hash.update(data.encode('utf-8'))

    # Get the hexadecimal representation of the hash
    hash_hex = sha256_hash.hexdigest()

    return hash_hex

# Example usage
if __name__ == "__main__":
    sample_data = "This is an example of data hashing!"
    hashed_data = hash_data(sample_data)
    print(f"Original data: {sample_data}")
    print(f"Hashed data: {hashed_data}")
