from cryptography.fernet import Fernet

key = Fernet.generate_key()
with open('key.txt', 'w') as arq:
	arq.write(key.decode('utf-8'))