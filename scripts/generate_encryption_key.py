from cryptography.fernet import Fernet

# Generate a Fernet key. should be 32 bit long
fernet_key = Fernet.generate_key()

print("Fernet Key:", fernet_key)
