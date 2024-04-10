import pytest
from src.core.Encryption import Encryption
from Crypto.Random import get_random_bytes
import json
import base64

def test_encryption():
    original_data = "This is a test."
    password = "securepassword".encode()
    salt = get_random_bytes(16)
    key = Encryption.derive_key(password, salt)

    encrypted_data = Encryption.encrypt_data(original_data, key)
    decrypted_data = Encryption.decrypt_data(encrypted_data, key)

    assert original_data == decrypted_data, "Original and decrypted data do not match"

def test_decryption_with_invalid_key():
    original_data = "This is a test."
    password = "securepassword".encode()
    salt = get_random_bytes(16)
    key = Encryption.derive_key(password, salt)
    encrypted_data = Encryption.encrypt_data(original_data, key)

    wrong_key = Encryption.derive_key("wrongpassword".encode(), salt)

    with pytest.raises(ValueError):
        Encryption.decrypt_data(encrypted_data, wrong_key)

def test_decryption_of_tampered_data():
    original_data = "This is a test."
    password = "securepassword".encode()
    salt = get_random_bytes(16)
    key = Encryption.derive_key(password, salt)
    encrypted_data_json = Encryption.encrypt_data(original_data, key)

    encrypted_data = json.loads(encrypted_data_json)
    encrypted_data['ciphertext'] = base64.b64encode(b"tampered" + base64.b64decode(encrypted_data['ciphertext'])).decode('utf-8')
    tampered_data_json = json.dumps(encrypted_data)

    with pytest.raises(ValueError):
        Encryption.decrypt_data(tampered_data_json, key)

def test_decryption_with_incorrect_nonce():
    original_data = "This is a test."
    password = "securepassword".encode()
    salt = get_random_bytes(16)
    key = Encryption.derive_key(password, salt)
    encrypted_data_json = Encryption.encrypt_data(original_data, key)

    encrypted_data = json.loads(encrypted_data_json)
    encrypted_data['nonce'] = base64.b64encode(get_random_bytes(16)).decode('utf-8')
    incorrect_nonce_data_json = json.dumps(encrypted_data)

    with pytest.raises(ValueError):
        Encryption.decrypt_data(incorrect_nonce_data_json, key)
        
def test_encryption_with_empty_data():
    password = "securepassword".encode()
    salt = get_random_bytes(16)
    key = Encryption.derive_key(password, salt)

    # The encryption of an empty string does not raise a ValueError by default.
    # If your application logic requires this, you need to implement this behavior in your Encryption.encrypt_data method.
    encrypted_data_json = Encryption.encrypt_data("", key)
    assert encrypted_data_json is not None, "Encryption should handle empty data properly"
