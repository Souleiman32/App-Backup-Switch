from cryptography.fernet import Fernet


def encrypt_password(password, key):
    # Chiffrement du mot de passe en utilisant la clé
    cipher = Fernet(key)
    encrypted_password = cipher.encrypt(password.encode())
    return encrypted_password.decode()


def decrypt_password(encrypted_password, key):
    # Déchiffrement du mot de passe en utilisant la clé
    cipher = Fernet(key)
    decrypted_password = cipher.decrypt(encrypted_password).decode()
    return decrypted_password

def get_key(key):
    # Récupération de la clé de chiffrement à partir d'un fichier
    with open(key, "rb") as key_file:
        key = key_file.read()
    return key
    
