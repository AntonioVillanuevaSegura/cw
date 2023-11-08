#Antonio Villanueva Segura cw pyhton linux
#pip install sounddevice
#pip install pynput

import numpy as np
import sounddevice as sd

import random
import time
import threading
from pynput import keyboard

TONE=900 #Hz
LIGNE=3 #Durée d'une ligne 
POINT=1 #Durée d'un point
SPACE=1#Espace entre les symboles
SPACE_MOTS=7 #Espace entre les mots
VITESSE=0.2

correcte=0
incorrecte=0

#dictionnaire de type clé (lettre), valeur (code cw)
cw_dict = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
    'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
    'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
    'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
    'Z': '--..',
    '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
    '6': '-....', '7': '--...', '8': '---..', '9': '----.', '0': '-----',
    '+': '.-.-.', '=': '-...-', ',': '--..--', '.': '.-.-.-', '?': '..--..',
    '/': '-..-.', '(': '-.--.', ')': '-.--.-', '&': '.-...',
    ':': '---...', ';': '-.-.-.', "'": '.----.', '-': '-....-',
    '_': '..--.-', '"': '.-..-.', '$': '...-..-', '!': '-.-.--',
    '@': '.--.-.'
}



touche=""
press=False

def on_press(key):
	global touche
	global press
	try:
		touche =format(key.char)
		press=True
	except AttributeError:
		print("Erreur ".format(key))


def on_release(key):
	global press

	press=False
	if key == keyboard.Key.esc:
		# Stop listener
		return False
        
def cw_aleatoire(cw):
	#renvoie une clé aléatoire dans le dictionnaire
	lettre=""
	while (not lettre.isalpha()):
		lettre=random.choice(list(cw.keys()))
	return lettre


def playSound(t):
	#joue un son de freq TONE et d'une durée t
	# Génère une tonalité sinusoïdale de la fréquence et de la durée spécifiées
	sin = np.linspace(0, t, int(t * 44100), endpoint=False)
	audio_data = 0.5 * np.sin(2 * np.pi * TONE * sin)

	# jouer le son
	sd.play(audio_data, 44100)

	# Attends la fin du son
	sd.wait()


def playChar(c,cw_dict):
	lettre= cw_dict[c]
	for s in lettre:
		if s=='.':
			playSound(POINT*VITESSE)
		else:
			playSound(LIGNE*VITESSE)
		time.sleep(SPACE*VITESSE)

def charCw (c,cw_dict):
	
	lettre= cw_dict[c]
	for s in lettre:
		if s=='.':
			print ('.',end="")
		else:
			print ('_',end="")
		print(' ',end="")			

	
def run():
	global press
	global touche
	global correcte
	global incorrecte

	while True:

		lettre=cw_aleatoire(cw_dict)
		charCw(lettre,cw_dict)
		playChar(lettre,cw_dict)
		print("Debug letra aleatoria =", lettre)
		
		#Wait for key press
		while not press:
			pass
			
		#wait until release the key		
		while  press:
			pass		
		
		if lettre==touche.upper():
			print (" OK",end="")
			correcte+=1
		else:
			print (" erreur, la lettre était ",lettre,end="")
			incorrecte+=1			
		print (" ( correctes = ",correcte," ,incorrectes =",incorrecte," )")
	
	
if __name__ == '__main__':

	with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
		hilo = threading.Thread(target=run)
		hilo.start()
		hilo.join()
		listener.join()	

	

