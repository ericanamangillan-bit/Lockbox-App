import random
import string
from flaskr.models.models import User, UserPasswords
from app import db

def generate_strong_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    return password

def custom_encrypt(text, shift=3):
    encrypted = ''.join(chr((ord(char) + shift - 32) % 95 + 32) for char in text)
    return encrypted

def custom_decrypt(text, shift=3):
    decrypted = ''.join(chr((ord(char) - shift - 32) % 95 + 32) for char in text)
    return decrypted

def custom_hash(password, salt):
    combined = password + salt
    hash_value = 0
    for char in combined:
        hash_value = (hash_value * 31 + ord(char)) % (2**32)
    return str(hash_value)