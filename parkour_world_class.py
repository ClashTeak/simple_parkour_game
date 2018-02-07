import pygame, sys , os , random
from pygame.locals import *
from math import cos,sin,pi


pygame.init()

WIN_WIDTH = 800
WIN_HEIGHT = 640
HALF_WIDTH = int(WIN_WIDTH / 2)
HALF_HEIGHT = int(WIN_HEIGHT / 2)

DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
DEPTH = 32
FLAGS = 0
CAMERA_SLACK = 30



class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)



# CAMERA CLASS.
class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


# ALL KIND OF CAMERA.
def simple_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    return Rect(-l+HALF_WIDTH, -t+HALF_HEIGHT, w, h)

def complex_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t, _, _ = -l+HALF_WIDTH, -t+HALF_HEIGHT, w, h

    l = min(0, l)                           # stop scrolling at the left edge
    l = max(-(camera.width-WIN_WIDTH), l)   # stop scrolling at the right edge
    t = max(-(camera.height-WIN_HEIGHT), t) # stop scrolling at the bottom
    t = min(0, t)                           # stop scrolling at the top
    return Rect(l, t, w, h)
    



#PLAYER CLASS
class Player(Entity):
    def __init__(self, x, y,size):
        Entity.__init__(self)
        self.xvel = 0
        self.yvel = 0
        self.onGround = False
        self.image = pygame.Surface((size,size))
        self.image.fill(Color("#0000FF"))
        self.image.convert()
        self.rect = Rect(x, y, size, size)

    def update(self, up, down, left, right, running, platforms):
        if up:
            # only jump if on the ground
            if self.onGround: self.yvel -= 8
        if down:
            pass
        if running:
            self.xvel = 12
        if left:
            self.xvel = -5
        if right:
            self.xvel = 5
        if not self.onGround:
            # only accelerate with gravity if in the air
            self.yvel += 0.3
            # max falling speed
            if self.yvel > 100: self.yvel = 100
        if not(left or right):
            self.xvel = 0
        # increment in x direction
        self.rect.left += self.xvel
        # do x-axis collisions
        self.collide(self.xvel, 0, platforms)
        # increment in y direction
        self.rect.top += self.yvel
        # assuming we're in the air
        self.onGround = False;
        # do y-axis collisions
        self.collide(0, self.yvel, platforms)

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if xvel > 0:
                    self.rect.right = p.rect.left
                    print ("collide right")
                if xvel < 0:
                    self.rect.left = p.rect.right
                    print ("collide left")
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0
                if yvel < 0:
                    self.rect.top = p.rect.bottom




#WORLD CLASS :

#block object class
class Block(Entity):
	
	def __init__(self,x,y,img,size):
		Entity.__init__(self)
		self.image = img
		self.rect = Rect(x, y, size, size)


#World Manager
class Niveau:
	"""Classe permettant de créer un niveau"""
	
	def __init__(self, fichier,tex):
		self.fichier = fichier
		self.structure = 0
		
		self.textures = tex
		
		self.taille_sprite = 32
		
		self.world_block = []
		
	def read(self):
		""" Méthode permettant de lire 
		le niveau en fonction du fichier.
		On crée une liste générale, contenant une liste par ligne 
		à afficher
		"""
		with open(self.fichier, "r") as fichier:
			structure_niveau = []
			#self.array_world = fichier.read()
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
					self.world_block.append(Block(x,y,self.textures[0],self.taille_sprite))
				if sprite == '2':
					self.world_block.append(Block(x,y,self.textures[1],self.taille_sprite))
				if sprite == '3':
					self.world_block.append(Block(x,y,self.textures[2],self.taille_sprite))
				num_case += 1
			num_ligne += 1
