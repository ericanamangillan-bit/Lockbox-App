import pytest
import string
from flaskr.service.services import generate_strong_password, custom_encrypt, custom_decrypt, custom_hash

def test_generate_strong_password():
    password = generate_strong_password()
    assert len(password) == 12
    assert any(c.islower() for c in password)
    assert any(c.isupper() for c in password)
    assert any(c.isdigit() for c in password)
    assert any(c in string.punctuation for c in password)

def test_custom_encrypt_decrypt():
    text = 'testpassword'
    encrypted = custom_encrypt(text)
    decrypted = custom_decrypt(encrypted)
    assert text == decrypted

def test_custom_hash():
    password = 'testpassword'
    salt = 'testsalt'
    hashed = custom_hash(password, salt)
    assert password != hashed
    assert salt != hashed