import pygame, sys , os , random
from pygame.locals import *


pygame.init()


class Physics():
	
	def __init__(self):
		self.velocity = 0.2
		self.IsGravity = True
	
	def onGravity(self,l):
		
		if self.IsGravity:
			for obj in l:
				if obj.have_gravity:
					obj.ys += self.velocity
		else:
			print("No Gravity !")
				


class Joueur(pygame.sprite.Sprite):
	
	def __init__(self,x ,y,image):
		self.x = x
		self.y = y
		self.xs, self.ys = 0,0
		
		self.have_gravity = True
		
		self.image = image
		
		self.update()
	
	def update(self):
		
		self.x += self.xs
		self.y += self.ys
		
		self.rect = (int(self.x),int(self.y),self.image.get_width(),self.image.get_height())
		self.mask = pygame.mask.from_surface(self.image)
	
	def jump(self):
		self.ys = -5
	
	def draw(self,surface):
		surface.blit(self.image,self.rect)



class Niveau:
	"""Classe permettant de créer un niveau"""
	
	def __init__(self, fichier, h, t, p):
		self.fichier = fichier
		self.structure = 0
		
		self.herbe = h
		self.terre = t
		self.pierre = p
		
		self.taille_sprite = 20
		
	def read(self):
		""" Méthode permettant de lire 
		le niveau en fonction du fichier.
		On crée une liste générale, contenant une liste par ligne 
		à afficher
		"""
		with open(self.fichier, "r") as fichier:
			structure_niveau = []
			
			for ligne in fichier:
				ligne_niveau = []
				
				for sprite in ligne:
					if sprite != '\n':
						ligne_niveau.append(sprite)
				structure_niveau.append(ligne_niveau)
			self.structure = structure_niveau
	
	
	def afficher(self, window):
		"""Méthode permettant d'afficher le niveau en fonction 
		de la liste de structure renvoyée par generer()
		"""
		#On parcourt la liste du niveau
		num_ligne = 0
		for ligne in self.structure:
			#On parcourt les listes de lignes
			num_case = 0
			for sprite in ligne:
				#On calcule la position réelle en pixels
				x = num_case * self.taille_sprite
				y = num_ligne * self.taille_sprite
				if sprite == '1':		   
					window.blit(self.terre, (x,y))
				if sprite == '2':
					window.blit(self.pierre, (x,y))
				if sprite == '3':
					window.blit(self.herbe, (x,y))
				num_case += 1
			num_ligne += 1
