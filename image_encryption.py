from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os

def encrypt_image(image_path, key, iv):
    # Read the image file
    with open(image_path, 'rb') as file:
        image_data = file.read()

    # Initialize the AES cipher
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Pad the image data to be a multiple of the block size
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(image_data) + padder.finalize()

    # Encrypt the padded data
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    # Write the encrypted data to a file
    with open('encrypted_image.enc', 'wb') as file:
        file.write(encrypted_data)

def decrypt_image(encrypted_path, key, iv, output_path):
    # Read the encrypted file
    with open(encrypted_path, 'rb') as file:
        encrypted_data = file.read()

    # Initialize the AES cipher
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    # Decrypt the data
    decrypted_padded_data = decryptor.update(encrypted_data) + decryptor.finalize()

    # Unpad the decrypted data
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()

    # Write the decrypted data to a file
    with open(output_path, 'wb') as file:
        file.write(decrypted_data)

# Generate a random key and IV
key = os.urandom(32)  # 256-bit key for AES-256
iv = os.urandom(16)   # 128-bit IV

# Paths for the input and output images
image_path = 'input_image.png' #paste your image name here
encrypted_path = 'encrypted_image.enc'
decrypted_path = 'decrypted_image.png'

# Encrypt the image
encrypt_image(image_path, key, iv)

# Decrypt the image
decrypt_image(encrypted_path, key, iv, decrypted_path)

print("Encryption and Decryption completed.")
