import random
import string


def generate_strong_password(length=12):
    if length < 1:
        raise ValueError("Password length must be positive")
    characters = string.ascii_letters + string.digits + string.punctuation
    while True:
        password = ''.join(random.choice(characters) for i in range(length))
        if (any(c.islower() for c in password) and
            any(c.isupper() for c in password) and
            any(c.isdigit() for c in password) and
            any(c in string.punctuation for c in password)):
            return password
#  generate a strong password with a length of 12 characters

def custom_encrypt(text, shift=3):
    if text is None:
        raise ValueError("Input text cannot be None")
    return ''.join(chr((ord(char) + shift - 32) % 95 + 32) for char in text)
# ecrypts the input text with a caesar cipher shift of 3

def custom_decrypt(text, shift=3):
    if text is None:
        raise ValueError("Input text cannot be None")
    return ''.join(chr((ord(char) - shift - 32) % 95 + 32) for char in text)
# decrypts the input text with a caesar cipher shift of 3

def custom_hash(password, salt):
    if password is None:
        raise ValueError("Password cannot be None")
    combined = str(password) + str(salt)
    hash_value = 0
    for char in combined:
        hash_value = (hash_value * 31 + ord(char)) % (2**32)
    return str(hash_value)
# hashes the input password with the input salt