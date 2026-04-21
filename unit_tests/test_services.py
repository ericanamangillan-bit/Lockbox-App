import pytest
import string
from flaskr.service.services import generate_strong_password, custom_encrypt, custom_decrypt, custom_hash

def test_generate_strong_password():
    password = generate_strong_password()
    assert len(password) == 12
    assert any(c.islower() for c in password), "Password must contain at least one lowercase letter"
    assert any(c.isupper() for c in password), "Password must contain at least one uppercase letter"
    assert any(c.isdigit() for c in password), "Password must contain at least one digit"
    assert any(c in string.punctuation for c in password), "Password must contain at least one special character"

def test_custom_encrypt_decrypt():
    # define test text
    text = 'testpassword'
    
    # encrypt the text
    encrypted = custom_encrypt(text)
    
    # decrypt the encrypted text
    decrypted = custom_decrypt(encrypted)
    
    # verify decryptred matches original
    assert text == decrypted

def test_custom_hash():
    # setup test data
    password = 'testpassword'
    salt = 'testsalt'
    
    # generate hash
    hashed = custom_hash(password, salt)
    
    # verify hash differs from inputs
    assert password != hashed
    assert salt != hashed
    
    # verify consistent hashing
    assert custom_hash(password, salt) == hashed
