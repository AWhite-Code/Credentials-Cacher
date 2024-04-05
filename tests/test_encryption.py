import pytest
from Encryption import Encryption
from Crypto.Random import get_random_bytes

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
    encrypted_data = Encryption.encrypt_data(original_data, key)

    encrypted_data['ciphertext'] = b"tampered" + encrypted_data['ciphertext']

    with pytest.raises(ValueError):
        Encryption.decrypt_data(encrypted_data, key)

def test_decryption_with_incorrect_nonce():
    original_data = "This is a test."
    password = "securepassword".encode()
    salt = get_random_bytes(16)
    key = Encryption.derive_key(password, salt)
    encrypted_data = Encryption.encrypt_data(original_data, key)

    encrypted_data['nonce'] = get_random_bytes(16)

    with pytest.raises(ValueError):
        Encryption.decrypt_data(encrypted_data, key)