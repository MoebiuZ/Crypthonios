import ui
import dialogs
import console
import os
import sys
from modules.crypthon import Crypthon

DATA_PATH = "encrypted/"

if not os.path.exists(DATA_PATH):
	os.makedirs(DATA_PATH)


database = Crypthon(DATA_PATH, "1&9qBCeEmo9redWcymV!1D5XL57Iw(Tu")
database.create_tables()

#database.insert_text("Una nota", "este es mi mensaje")
def pluf(sender):
	console.clear()
	# hack to crash Pythonista
	os.abort()
	
v = ui.load_view('views/list').present('fullscreen', hide_title_bar=True, orientations=['portrait'])

if database.isNew():
	passwd_dlg = dialogs.form_dialog(title='Create a password',fields=[{'type':'password','title':'New password', 'key':'password'}])
	database.set_password(passwd_dlg["password"])
else:
	correct = False
	while not correct:
		passwd_dlg = dialogs.form_dialog(title='Enter your password',fields=[{'type':'password','title':'Password', 'key':'password'}])
	
		#if passwd_dlg == None:
		#exit()
		
			
		correct = database.login(passwd_dlg['password'])
		
		if correct:
			console.hud_alert('OK')
		
