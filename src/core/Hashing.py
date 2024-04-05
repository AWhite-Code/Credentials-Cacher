from Crypto.Hash import SHA256
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
import base64

class Hashing:
    """
    Provides functionality for hashing and verifying passwords securely.
    """
    
    @staticmethod
    def hash_password(password):
        """
        Hashes a password using PBKDF2-SHA256, generating a random salt for each new hash.

        Args:
            password (str): The password to be hashed.

        Returns:
            str: The hashed password in a storage format that includes the salt and the hash, separated by "::".
        """
        # Generate a random salt
        salt = get_random_bytes(16)
        # Hash the password with the salt using PBKDF2-SHA256
        key = PBKDF2(password, salt, dkLen=32, count=100000, hmac_hash_module=SHA256)
        # Store the salt and the hash key together, separated by "::"
        storage_format = base64.b64encode(salt).decode() + "::" + base64.b64encode(key).decode()
        return storage_format

    @staticmethod
    def verify_password(stored_password, provided_password):
        """
        Verifies a provided password against a stored password hash.

        Args:
            stored_password (str): The hashed password stored in the format "salt::hash".
            provided_password (str): The password provided for verification.

        Returns:
            bool: True if the provided password matches the stored hash, False otherwise.
        """
        # Extract the salt and key from the stored password format
        salt_encoded, key_encoded = stored_password.split("::")
        salt = base64.b64decode(salt_encoded)
        key = base64.b64decode(key_encoded)
        # Hash the provided password with the extracted salt
        new_key = PBKDF2(provided_password, salt, dkLen=32, count=100000, hmac_hash_module=SHA256)
        # Compare the new key with the extracted key
        return key == new_key
