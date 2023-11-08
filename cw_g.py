#Antonio Villanueva Segura CW 
#!/usr/bin/env python3
# -*- coding: utf-8

"""
sudo apt install python3-pip
pip install sounddevice
pip install pynput
pip install tk
pip install numpy

"""

import tkinter as tk
from tkinter import ttk

import numpy as np
import sounddevice as sd

import threading
import time
import random

TONE=900 #Hz
LIGNE=3 #Durée d'une ligne 
POINT=1 #Durée d'un point
SPACE=1#Espace entre les symboles
SPACE_MOTS=7 #Espace entre les mots
WIDTH_TEXT=92 #Taille X afficheur text

VITESSE=0.1

class cw():
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

	def __init__(self):
		super().__init__()
		self.vitesse=VITESSE
		self.tone=TONE

	def setVitesse(self,vitesse):
		self.vitesse=vitesse
		
	def setTone(self,tone):
		self.tone=tone
				
	def cw_aleatoire(self,limite):
		"""renvoie une clé aléatoire dans le dictionnaire"""
		lettre=""
		if limite==0:
			while (not lettre.isalpha()):
				lettre=random.choice(list(self.cw_dict.keys()))
		else:
			lettre=random.choice(list(self.cw_dict.keys()))
		return lettre

	def playSound(self,t):
		"""joue un son de freq TONE et d'une durée t"""
		# Génère une tonalité sinusoïdale de la fréquence et de la durée spécifiées
		sin = np.linspace(0, t, int(t * 44100), endpoint=False)
		audio_data = 0.5 * np.sin(2 * np.pi * self.tone * sin)

		# jouer le son
		sd.play(audio_data, 44100)

		# Attends la fin du son
		sd.wait()

	def playChar(self,c):
		"""joue une lettre en télégraphie"""
		lettre= self.cw_dict[c]
		for s in lettre:
			if s=='.':
				self.playSound(POINT*self.vitesse)
			else:
				self.playSound(LIGNE*self.vitesse)
			time.sleep(SPACE*self.vitesse)		

	def charCw (self, c):
		""" equivalence cw"""		
		return self.cw_dict[c]		
			
class InterfaceGraphique(tk.Tk):
	def __init__(self):
		super().__init__()
		self.motpm=0
		self.creeGui() #Cree GUI tkinter
		self.cw=cw() #classe CW instance
		#Thread generation mots
		#self.fil = threading.Thread(target=self.envoiMots)
		#self.fil.daemon = True  # Le fil "thread" s'arrêtera à la fermeture de l'application
		
	def creeGui(self):
		""" Crée l'interface utilisateur avec tkinter"""
		#variables
		self.time_old=time.mktime(time.localtime())
		self.time_old2=time.mktime(time.localtime())		
		self.mpm=tk.IntVar()
		self.vitesse = tk.DoubleVar() #Vitesse
		self.tone=tk.IntVar() #Tone 
		self.space_mots=tk.IntVar() #space entre mots groups
		self.option = tk.IntVar()
						
		#defaults values
		self.mpm.set(0) #mots par minute
		self.vitesse.set(VITESSE) #vitesse relative default VITESSE
		self.tone.set (TONE) #Tone default TONE
		self.space_mots.set(5) #Default 5
		
		#Window					
		#tkinter window
		self.title('CW Antonio VILLANUEVA')
		self.resizable( False, False )
		self.geometry("750x250")
				
		#Frames		
		#Frame Sup Ctrls.
		self.FrameSup=tk.Frame(self, borderwidth=2)	
		self.FrameSup.pack()	
		
		#Frame Inf Text.
		self.FrameInf=tk.Frame(self, borderwidth=2)	
		self.FrameInf.pack()
		
		#Button Play	
		self.PLAYButton=tk.Button(self.FrameSup,text="PLAY", bg="red",
		command=lambda: self.play("PLAY"))		
		self.PLAYButton.grid(row=0,column=2,columnspan = 1)
		
		#Check button (utiliser tous les symboles ou uniquement les lettres)
		self.checkbutton = tk.Checkbutton(self.FrameSup, text="ALL CHARS", variable=self.option, onvalue=1, offvalue=0)
		self.checkbutton.grid(row=0,column=3,columnspan = 1)	
				
		#Labels		
		#Clock Label
		self.clock = tk.Label(self.FrameSup, bg="Black", fg="green")
		self.clock.grid(row=1,column=4,columnspan = 1)
		self.times()	
				
		#Mots par minute Label
		self.motspmLabel=tk.Label (self.FrameSup,text="ppm",justify="center")
		self.motspmLabel.grid(row=0,column=0)
		
		#Mots par minute Label Reel
		self.motspmRLabel=tk.Label (self.FrameSup,text="reel",justify="center")
		self.motspmRLabel.grid(row=0,column=1,columnspan = 1)		
		
		#Vitesse Label
		self.vitesseLabel=tk.Label (self.FrameSup,text="SPEED",justify="center")
		self.vitesseLabel.grid(row=1,column=0,columnspan = 1)	
		
		#Tone Label
		self.toneLabel=tk.Label (self.FrameSup,text="TONE",justify="center")
		self.toneLabel.grid(row=1,column=1)
		
		#CW Label		
		self.cwLabel=tk.Label (self.FrameSup,text="CW",justify="center")
		#fontStyle.configure(size=fontsize + 2
		#self.cwLabel.configure(size = 100)
		self.cwLabel.configure (font=("", 25))
		self.cwLabel.grid(row=2,column=3)		
		
		#Mots Space Label
		self.toneLabel=tk.Label (self.FrameSup,text="SPACE WORDS",justify="center")
		self.toneLabel.grid(row=1,column=2)		
				
		#Scale vitesse mots pm
		self.VitesseScale = tk.Scale( self.FrameSup, variable = self.vitesse, from_ = 0.08, to = 0.2,resolution = 0.01, orient = "horizontal")
		self.VitesseScale.grid(row=2,column=0,columnspan = 1)
		
		#TONE
		self.ToneScale = tk.Scale( self.FrameSup, variable = self.tone, from_ = 700, to = 1000, orient = "horizontal")
		self.ToneScale.grid(row=2,column=1,columnspan = 1)		
		
		#SPACE MOTS
		self.SpaceMotsScale = tk.Scale( self.FrameSup, variable = self.space_mots, from_ = 1, to = 10, orient = "horizontal")
		self.SpaceMotsScale.grid(row=2,column=2,columnspan = 1)		
		
		#TEXT
		self.Texte=tk.Text(self.FrameInf,width=WIDTH_TEXT,height=8,state="normal",yscrollcommand=True)
		#self.Texte.(yscrollcommand=True)
		self.Texte.grid(row=1,column=1,columnspan = 1)

	def envoiMots(self):
		"""Pendant PLAY est en lecture, il joue les mots cw"""
		# fonctionne dans un thread !! 
		# self.fil = threading.Thread(target=self.envoiMots)
		
		text_space=1 #counteur mots , group
		nmots=0 #nombre de mots
 
		self.cw.setTone(self.tone.get())
		self.cw.setVitesse(self.vitesse.get())
		
		while self.PLAYButton.cget('text') == "PAUSE":
			lettre= self.cw.cw_aleatoire(self.option.get()) #lettre aleatoire
			self.cwLabel.config (text= self.cw.charCw (lettre))
			
			self.cw.playChar(lettre) #play lettre sound
			
			self.cw.setTone(self.tone.get())# set tone freq.
			self.cw.setVitesse(self.vitesse.get())#set vitesse		
					
			self.Texte.insert(tk.END, lettre)  # Ajoute la lettre au panneu text		
			self.update()
			
			#Space entre mots 
			if text_space>=self.space_mots.get():
				self.Texte.insert(tk.END, " ")  # Ajoute space	
				self.update()
				text_space=1
				time.sleep(SPACE_MOTS*self.vitesse.get()) 
			else:
				text_space +=1
			
			nmots+=1
			self.calculMotsPm(nmots) #Relative
			
			#Calcul des mots par minute Reel
			if time.time() - self.time_old2 >= 60:# 1 minute
			 self.time_old2= time.time()
			 self.motspmRLabel.config (text=nmots)#Set char par minute
			 nmots =0
			 
			
			time.sleep(SPACE*self.vitesse.get()) #space mots , group sleep

		print ("stop thread ")
					
	def play(self,st):
		""" play-pause button"""
		text= self.PLAYButton.cget('text')
		#fil = threading.Thread(target=self.envoiMots)
		if text=="PLAY":
			self.PLAYButton.configure( bg="green" )#couleur 
			self.PLAYButton.configure( text="PAUSE" )#text
			
			#Run Thread envoiMots jusqu'a PAUSE
			self.fil = threading.Thread(target=self.envoiMots)
			self.fil.daemon = True  # Le fil "thread" s'arrêtera à la fermeture de l'application
			self.fil.start()
			#print ("Debug Threads actives ", threading.enumerate())
		
		else:
			
			#print ("Debug Threads actives ", threading.enumerate())

			self.PLAYButton.configure( bg="red" )
			self.PLAYButton.configure( text="PLAY" )
		
	def times(self)	:#clock
		""" Contrôle de l'horloge """
		current_time=time.strftime ('%H:%M:%S')
		self.clock.config(text=current_time)
		self.clock.after(500,self.times)

	def tempsEcouleSec (self):
		"""Calculer le temps écoulé en secondes """
		temps_actuel = time.localtime() 
		temps_secondes = time.mktime(temps_actuel)
		
		tmp =temps_secondes - self.time_old
		self.time_old=temps_secondes
		return tmp		
		
	def calculMotsPm(self,nmots):
		""" Calcul des mots par minute Relative"""
		tmp=0
		ecoule=self.tempsEcouleSec ()
		if nmots>0 and ecoule>0 :		
			tmp=1*60/ecoule
			self.motspmLabel.config(text= round (tmp) )
									
if __name__ == "__main__":
  app = InterfaceGraphique() #Instance InterfaceGraphique tkinter
  app.mainloop() #tkinter main loop
