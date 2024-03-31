from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
from Crypto.Hash import SHA256
import base64

class Encryption:
    @staticmethod
    def derive_key(password, salt):
        key_length = 32  # Key length for AES-256
        iterations = 100000
        return PBKDF2(password, salt, dkLen=key_length, count=iterations, hmac_hash_module=SHA256)

    @staticmethod
    def encrypt_data(data: str, key: bytes) -> dict:
        salt = get_random_bytes(16)
        nonce = get_random_bytes(16)
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        ciphertext, tag = cipher.encrypt_and_digest(data.encode())
        return {'ciphertext': ciphertext, 'salt': salt, 'nonce': nonce, 'tag': tag}

    @staticmethod
    def decrypt_data(encrypted: dict, key: bytes) -> str:
        try:
            cipher = AES.new(key, AES.MODE_GCM, nonce=encrypted['nonce'])
            plaintext = cipher.decrypt_and_verify(encrypted['ciphertext'], encrypted['tag'])
            return plaintext.decode()
        except (ValueError, KeyError):
            # Raise ValueError to indicate decryption failure or missing data
            raise ValueError("Decryption failed due to incorrect key or tampering.")