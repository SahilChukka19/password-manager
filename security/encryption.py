from cryptography.fernet import Fernet

# Generate Key
def generate_key(key_path="config/secrets.key"):
    key = Fernet.generate_key()
    with open(key_path,'wb') as key_file:
        return key_file.write(key)

# Load Key
def load_key(key_path="config/secrets.key"):
    with open(key_path, 'rb') as key_file:
        return key_file.read()

# Encrypt Password
def encrypt_password(password, key):
    f = Fernet(key)
    return f.encrypt(password.encode())

# Decrypt Password 
def decrypt_password(password, key):
    f = Fernet(key)
    return f.decrypt(password.decode())

if __name__ == "__main__":
    generate_key()# Generate a key (run this only once to create the key file)
    print("Encryption key generated and saved!")



