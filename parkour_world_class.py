import pygame, sys , os , random
from pygame.locals import *
from math import cos,sin,pi
from parkour_world_settings import *

pygame.init()
            

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
    

class HUD(object):
	
	def __init__(self,width,heigth,surface,font):
		self.surface = surface
		self.width = width
		self.height = heigth
		self.font = font
	
	def health_bar(self,color1,color2,hp,maxhp):
		pygame.draw.rect(self.surface,color1,(self.width-(self.width-20),self.height-(self.height-(self.height/42)),self.width/3.2,self.height/42))
		pygame.draw.rect(self.surface,color2,(self.width-(self.width-20),self.height-(self.height-(self.height/42)),hp/(maxhp/(self.width/3.2)),self.height/42))
	
	def mana_bar(self,color1,color2,mana,maxmana):
		pygame.draw.rect(self.surface,color1,(self.width-(self.width-20),self.height-(self.height-(self.height/16)),self.width/3.2,self.height/42))
		pygame.draw.rect(self.surface,color2,(self.width-(self.width-20),self.height-(self.height-(self.height/16)),mana/(maxmana/(self.width/3.2)),self.height/42))
	
	def coins(self,coins,color,img):
		affiche_coins = self.font.render(str(coins),True,color)
		self.surface.blit(affiche_coins,(self.width-75,self.height/64))
		self.surface.blit(img,(self.width-40,self.height/32))


#PLAYER CLASS
class Player(Entity):
	def __init__(self, x, y,sizex,sizey):
		Entity.__init__(self)
		self.xvel = 0
		self.yvel = 0
		self.speed = 4
		self.coins = 0
		self.max_mana = 100
		self.mana = self.max_mana
		self.can_sprint = True
		self.max_hp = 100
		self.hp = self.max_hp
		self.onGround = False
		self.image = pygame.Surface((sizex,sizey))
		self.image.fill(Color("#0000FF"))
		self.image.convert()
		self.rect = Rect(x, y, sizex, sizey)
		self.jumpForce = 8

	def update(self, up, down, left, right, running, platforms,coins):
		if self.mana < 1:
			running = False
			self.speed = 4
			self.can_sprint = False
		if up:
			# only jump if on the ground
			if self.onGround: self.yvel -= self.jumpForce
		if down:
			pass
		if left:
			self.xvel = -self.speed
		if right:
			self.xvel = self.speed
		if not self.onGround:
			# only accelerate with gravity if in the air
			self.yvel += 0.3
			# max falling speed
			if self.yvel > 100: self.yvel = 100
		if not(left or right):
			self.xvel = 0
		if self.can_sprint == False:
			running = False
		if running:
			if self.can_sprint:
				self.speed = 7
				if left or right:
					if self.mana > 1:
						self.mana -= 0.6
		if not running:
			self.speed = 4
			if self.mana < self.max_mana:
				self.mana += 0.4
			else:
				if self.can_sprint == False:
					self.can_sprint = True
			
		# increment in x direction
		self.rect.left += self.xvel
		# do x-axis collisions
		self.collide(self.xvel, 0, platforms,coins)
		# increment in y direction
		self.rect.top += self.yvel
		# assuming we're in the air
		self.onGround = False;
		# do y-axis collisions
		self.collide(0, self.yvel, platforms,coins)
		
		if self.hp < 0:
			pygame.quit()
			sys.exit()
		
	def collide(self, xvel, yvel, colliders,coins):
		for p in colliders:
			if pygame.sprite.collide_rect(self, p):
				if p.name == "block":
					if xvel > 0:
						self.rect.right = p.rect.left
					if xvel < 0:
						self.rect.left = p.rect.right
					if yvel > 0:
						self.rect.bottom = p.rect.top
						self.onGround = True
						self.yvel = 0
					if yvel < 0:
						self.rect.top = p.rect.bottom
				elif p.name == "coin":
					self.coins += 1
					coins.remove(p)
					colliders.remove(p)
				elif p.name == "lava":
					self.hp -= 0.5




#WORLD CLASS :

#block object class
class Block(Entity):
	
	def __init__(self,x,y,img,size,name):
		Entity.__init__(self)
		self.image = img
		self.rect = Rect(x, y, size, size)
		self.name = name


#World Manager
class WorldManager:
	"""Classe permettant de créer un niveau"""
	
	def __init__(self,tex,bg_tex):
		self.structure = 0
		
		self.textures = tex
		self.bg_textures = bg_tex
		
		self.taille_sprite = 25
		self.level = 1
		
		self.world_block = []
		self.world_background_block = []
		
		self.try_collide = []
	
	def read(self,f):
		with open(f, "r") as fichier:
			structure_niveau = []
			#self.array_world = fichier.read()
			for ligne in fichier:
				ligne_niveau = []
				for sprite in ligne:
					if sprite != '\n':
						ligne_niveau.append(sprite)
				structure_niveau.append(ligne_niveau)
			self.structure = structure_niveau
	
	
	def generate(self,f,f_background):
		""" Méthode permettant de lire 
		le niveau en fonction du fichier.
		On crée une liste générale, contenant une liste par ligne 
		à afficher
		"""
		self.read(f)
		self.draw(self.world_block,self.textures)
		self.read(f_background)
		self.draw(self.world_background_block,self.bg_textures)
	
	def update(self,target):
		for b in self.world_block:
			if b.rect.x < target.rect.x + 70 and b.rect.x > target.rect.x - 70:
				if b.rect.y < target.rect.y + 70 and b.rect.y > target.rect.y - 70:
					if b not in self.try_collide:
						self.try_collide.append(b)
				else:
					if b in self.try_collide:
						self.try_collide.remove(b)
			else:
					if b in self.try_collide:
						self.try_collide.remove(b)
	
	def draw(self,l,textures):
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
				if sprite == '0':	
					l.append(Block(x,y,textures[int(sprite)],self.taille_sprite,"block"))
				if sprite == '1':
					l.append(Block(x,y,textures[int(sprite)],self.taille_sprite,"block"))
				if sprite == '2':
					l.append(Block(x,y,textures[int(sprite)],self.taille_sprite,"block"))
				if sprite == '3':
					l.append(Block(x,y,textures[int(sprite)],self.taille_sprite,"block"))
				if sprite == 'c':
					l.append(Block(x,y,textures[4],self.taille_sprite,"coin"))
				if sprite == 'l':
					l.append(Block(x,y,textures[5],self.taille_sprite,"lava"))
				num_case += 1
			num_ligne += 1


