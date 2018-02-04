import pygame, sys , os , random
from pygame.locals import *


pygame.init()
				


class Joueur(pygame.sprite.Sprite):
	
	def __init__(self,x ,y,image,velocity):
		self.x = x
		self.y = y
		self.xs, self.ys = 0,0
		
		self.have_gravity = True
		self.velocity = velocity
		
		self.isGrounded = False
		self.isJumping = False
		
		self.try_collide = []
		
		self.image = image
		
		self.rect = (int(self.x),int(self.y),self.image.get_width(),self.image.get_height())
		self.mask = pygame.mask.from_surface(self.image)
	
	def update(self,b_l):
		self.rect = (int(self.x),int(self.y),self.image.get_width(),self.image.get_height())
		
		
		for b in b_l:
			if b.x < self.x + 21 and b.x > self.x - 21:
				if b.y < self.y + 21 and b.y > self.y - 21:
					if b not in self.try_collide:
						self.try_collide.append(b)
				else:
					if b in self.try_collide:
						self.try_collide.remove(b)
			else:
				if b in self.try_collide:
					self.try_collide.remove(b)
		
		if len(self.try_collide) != 0:
			for b in self.try_collide:
				if pygame.sprite.collide_mask(self,b) == False:
					self.isGrounded = False
				elif pygame.sprite.collide_mask(self,b):
					self.isGrounded = True
					self.y = b.y - 20
		else:
			self.isGrounded = False
			
		print(len(self.try_collide))
		
		if self.isGrounded == False:
			if self.have_gravity:
				self.ys += self.velocity
		
		if self.isGrounded:
			self.y -= self.ys
			self.ys = 0
			
		self.y += self.ys
		self.x += self.xs
		
		self.mask = pygame.mask.from_surface(self.image)
	
	def jump(self):
		if self.isGrounded:
			self.isJumping = True
			self.isGrounded = False
			self.ys = -5
			self.y -= 5
	
	def draw(self,surface):
		surface.blit(self.image,self.rect)
		


class Block(pygame.sprite.Sprite):
	
	def __init__(self,x,y,img):
		self.x,self.y = x,y
		self.image = img
		self.mask = pygame.mask.from_surface(self.image)
		self.rect = (int(x),int(y),self.image.get_width(),self.image.get_height())


class Niveau:
	"""Classe permettant de créer un niveau"""
	
	def __init__(self, fichier,tex):
		self.fichier = fichier
		self.structure = 0
		
		self.textures = tex
		
		self.taille_sprite = 20
		
		self.world_block = []
		self.print_block = []
		
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
	
	
	def afficher(self):
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
					self.world_block.append(Block(x,y,self.textures[0]))
				if sprite == '2':
					self.world_block.append(Block(x,y,self.textures[1]))
				if sprite == '3':
					self.world_block.append(Block(x,y,self.textures[2]))
				num_case += 1
			num_ligne += 1
	
	def update(self,joueur):
		
		for b in self.world_block:
			if b.x < joueur.x + 700 and b.x > joueur.x - 700:
				if b.y < joueur.y + 500 and b.y > joueur.y - 500:
					if b not in self.print_block:
						self.print_block.append(b)
				else:
					if b in self.print_block:
						self.print_block.remove(b)
			else:
				if b in self.print_block:
					self.print_block.remove(b)
			
