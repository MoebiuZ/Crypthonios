# -*- coding: utf-8 -*- #

import sqlite3
import hashlib
import struct
import os
import gc
import ctypes
from Crypto.Cipher import AES

from Crypto.Util.py3compat import *



class Crypthon:

	SALT32 = b"1&9qBCeEmo9redWcymV!1D5XL57Iw(Tu"

	
	def __init__(self, data_path, salt):
		

		AES.block_size = 32
		self.SALT32 = salt.encode()
		self.password = ""
		self.key = ""
		
		self.data_path = data_path.strip("/")
		
		if not os.path.exists(self.data_path):
			os.makedirs(self.data_path)

		self.conn = sqlite3.connect(self.data_path + "/notes.sqlite")
		self.conn.row_factory = sqlite3.Row
		self.c = self.conn.cursor()




	def create_tables(self):
		self.c.execute('''CREATE TABLE IF NOT EXISTS config (
			id INTEGER PRIMARY KEY CHECK (id = 0),
			check_password blob NOT NULL DEFAULT "") ''')

		self.c.execute('''CREATE TABLE IF NOT EXISTS entry (
			type integer NOT NULL DEFAULT 0, 
			name blob NOT NULL,
			data blob NOT NULL) ''')


		self.conn.commit()



	def encrypt_text(self, data):
		iv = os.urandom(16)
		encryptor = AES.new(self.key, AES.MODE_CBC, IV=iv)

		encrypted = encryptor.encrypt(self.pcks7_pad(data))
		return encrypted + iv


	def encrypt_file(self, data):
		iv = os.urandom(16)

		return encrypted + iv



	def decrypt_text(self, data):

		decryptor = AES.new(self.key, AES.MODE_CBC, IV = data[-16:])
		decrypted = self.pcks7_unpad(decryptor.decrypt(data[:-16]))

		return decrypted

	
	def decrypt_file(self, data):
		pass




	def pcks7_pad(self, data_to_pad):
		padding_len = AES.block_size - len(data_to_pad) % AES.block_size
		padding = bchr(padding_len) * padding_len

		return data_to_pad + padding



	def pcks7_unpad(self, padded_data):
		pdata_len = len(padded_data)
		if pdata_len % AES.block_size:
			raise ValueError("Input data is not padded")

		padding_len = bord(padded_data[-1])

		if padding_len < 1 or padding_len > min(AES.block_size, pdata_len):
			pass
			#raise ValueError("Padding is incorrect.")

		if padded_data[-padding_len:] != bchr(padding_len) * padding_len:
			pass
			#raise ValueError("PKCS#7 padding is incorrect.")

		return padded_data[:-padding_len]




	def login(self, password):

		self.key = hashlib.pbkdf2_hmac('sha256', password.encode(), self.SALT32, 100000)


		# Clear mem
		password = os.urandom(len(password))
		gc.collect()



		self.c.execute("SELECT check_password FROM config")
		data = self.c.fetchone()
		

		decrypted = self.decrypt_text(data[0])
		
		
	
		if decrypted == b"Correcto":
			return True
		else:
			return False



	def set_password(self, password):

		self.key = hashlib.pbkdf2_hmac('sha256', password.encode(), self.SALT32, 100000)

		self.c.execute("INSERT INTO config values(0, ?)", [self.encrypt_text(b"Correcto")])
		self.conn.commit()
		# Clear mem
		password = os.urandom(len(password))
		gc.collect()



	def change_password(self, old_password, new_password):

		self.key = hashlib.pbkdf2_hmac('sha256', new_password.encode(), self.SALT32, 100000)

		# Clear mem
		old_password = os.urandom(len(old_password))
		new_password = os.urandom(len(new_password))
		gc.collect()





	def insert_text(self, title, data):

		self.c.execute("INSERT INTO entry values(0, ?, ?)", [self.encrypt_text(title.encode()), self.encrypt_text(data.encode())])
		self.conn.commit()


	def insert_file(self, path):
		
		filename_w_ext = os.path.basename(path)
		filename = os.path.splitext(filename_w_ext)
		filename = os.path.path
		encrypted_filename = hashlib.sha256(title,encode()).digest()

		self.c.execute("INSERT INTO entry values(0, ?, ?)", [self.encrypt_text(filename.encode()), encrypted_filename])
		self.conn.commit()


	def isNew(self):
		self.c.execute("SELECT check_password FROM config")
		result = self.c.fetchone()
		
		if result == None:
			return True
		else:
			return False
		
		
	def exit_and_clear(self):
		self.key = os.urandom(len(self.key))
		gc.collect()





# For maximal security, the IV should be randomly generated for every new encryption and can be stored together with the ciphertext.
#IV = 16 * '\x00'


'''
key = hashlib.pbkdf2_hmac('sha256', password.encode(), database.SALT32, 100000)


iv =  os.urandom(16)





data = b"asdaaaaaaaaaaaaaaaaaaaabaaaaaaaaaaaaaaaaaaaaaaaaaaaaiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiccuhciuhascihaischaicuhasikchaicuhaihciauhciashciasuchaishciahcaiuchaiushciauchaichaisuhc"
zum = database.pcks7_pad(data)


		
print(zum)

print(database.pcks7_unpad(zum))

encryptor = AES.new(key, AES.MODE_CBC, IV=iv)

text = 'j' * 64 + 'i' * 128
print(encryptor.encrypt(text))
print(encryptor.encrypt(text))

'''

#print(ciphertext)

#print(encryptor.decrypt(ciphertext))
