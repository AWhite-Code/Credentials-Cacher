from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
from Crypto.Hash import SHA256

class Encryption:
    @staticmethod
    def derive_key(password, salt):
        """
        Derives an AES-256 key from the given password and salt.
        
        Args:
            password (str): The master password.
            salt (bytes): A cryptographic salt.
        
        Returns:
            bytes: The derived AES-256 key.
        """
        key_length = 32  # Key length for AES-256
        iterations = 100000  # Number of iterations for PBKDF2
        
        key = PBKDF2(password, salt, dkLen=key_length, count=iterations, hmac_hash_module=SHA256)
        return key

    @staticmethod
    def encrypt_data(data: str, key: bytes) -> dict:
        """
        Encrypt data using AES-256 GCM mode.
        Returns a dictionary with 'ciphertext', 'salt', and 'nonce'.
        """
        salt = get_random_bytes(16)
        nonce = get_random_bytes(16)  # GCM nonce
        derived_key = Encryption.derive_key(key, salt)
        cipher = AES.new(derived_key, AES.MODE_GCM, nonce=nonce)
        ciphertext, tag = cipher.encrypt_and_digest(data.encode())
        return {
            'ciphertext': ciphertext,
            'salt': salt,
            'nonce': nonce,
            'tag': tag
        }

    @staticmethod
    def decrypt_data(encrypted: dict, key: bytes) -> str:
        """
        Decrypt data encrypted by encrypt_data.
        Expects a dictionary with 'ciphertext', 'salt', 'nonce', and 'tag'.
        """
        derived_key = Encryption.derive_key(key, encrypted['salt'])
        cipher = AES.new(derived_key, AES.MODE_GCM, nonce=encrypted['nonce'])
        plaintext = cipher.decrypt_and_verify(encrypted['ciphertext'], encrypted['tag'])
        return plaintext.decode()
    