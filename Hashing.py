from Crypto.Hash import SHA256
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
import base64

class Hashing:
    @staticmethod
    def hash_password(password):
        # Generate a random salt
        salt = get_random_bytes(16)
        # Hash the password with the salt using PBKDF2-SHA256
        key = PBKDF2(password, salt, dkLen=32, count=100000, hmac_hash_module=SHA256)
        # Store the salt and the hash key together, separated by "::"
        storage_format = base64.b64encode(salt).decode() + "::" + base64.b64encode(key).decode()
        return storage_format

    @staticmethod
    def verify_password(stored_password, provided_password):
        # Extract the salt and key from the stored password format
        salt_encoded, key_encoded = stored_password.split("::")
        salt = base64.b64decode(salt_encoded)
        key = base64.b64decode(key_encoded)
        # Hash the provided password with the extracted salt
        new_key = PBKDF2(provided_password, salt, dkLen=32, count=100000, hmac_hash_module=SHA256)
        # Compare the new key with the extracted key
        return key == new_key