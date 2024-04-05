import json
import base64
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
from Crypto.Hash import SHA256
import logging

# Setup basic logging
logging.basicConfig(filename='app.log', level=logging.DEBUG, 
                    format='%(asctime)s %(levelname)s %(message)s')

class Encryption:
    @staticmethod
    def derive_key(password, salt):
        """
        Derive an AES-256 encryption key from a password and salt.
        """
        key_length = 32  # AES-256 requires a key size of 32 bytes.
        iterations = 100000
        key = PBKDF2(password, salt, dkLen=key_length, count=iterations, hmac_hash_module=SHA256)
        return key

    @staticmethod
    def encrypt_data(data: str, key: bytes) -> str:
        """
        Encrypt the provided data using AES-256 GCM mode.
        """
        salt = get_random_bytes(16)  # Not used in GCM mode, but included for completeness.
        nonce = get_random_bytes(16)
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        ciphertext, tag = cipher.encrypt_and_digest(data.encode())
        
        encrypted_data = json.dumps({
            'ciphertext': base64.b64encode(ciphertext).decode('utf-8'),
            'nonce': base64.b64encode(nonce).decode('utf-8'),
            'tag': base64.b64encode(tag).decode('utf-8'),
        })
        #logging.debug(f"Serialized encrypted data: {encrypted_data}")
        return encrypted_data

    @staticmethod
    def decrypt_data(encrypted: str, key: bytes) -> str:
        if key is None:
            logging.error("Encryption key is None. Decryption cannot proceed.")
            return "" 
        if encrypted is None:
            logging.error("Encrypted data is None. Decryption cannot proceed.")
            return "" 
        try:
            #logging.debug(f"Encrypted data received for decryption: {encrypted}")
            encrypted_dict = json.loads(encrypted)
            nonce = base64.b64decode(encrypted_dict['nonce'])
            tag = base64.b64decode(encrypted_dict['tag'])
            ciphertext = base64.b64decode(encrypted_dict['ciphertext'])
            cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
            plaintext = cipher.decrypt_and_verify(ciphertext, tag)
            #logging.debug(f"Decrypted data: {plaintext.decode()}")
            return plaintext.decode()
        except (ValueError, KeyError) as e:
            #logging.error(f"Decryption failed: {e}")
            raise ValueError("Decryption failed due to incorrect key or tampering.")