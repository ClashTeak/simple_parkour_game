import pygame, sys, os, random
from pygame.locals import *
from parkour_world_class import *

pygame.init()


window = pygame.display.set_mode(DISPLAY, FLAGS, DEPTH)
clock = pygame.time.Clock()

#all textures about the environment:
WORLD_IMG = [
	pygame.transform.scale(pygame.image.load("Data/Pictures/world_textures/grass.png"),(25,25)),#GRASS
	pygame.transform.scale(pygame.image.load("Data/Pictures/world_textures/dirt.png"),(25,25)),#DIRT
	pygame.transform.scale(pygame.image.load("Data/Pictures/world_textures/stone.png"),(25,25)),#STONE
]
#all futures and currents levels:
LEVELS = [
	"parkour_world_lvl1",
	"parkour_world_lvl2",
	"parkour_world_lvl3",
	"parkour_world_lvl4",
	"parkour_world_lvl5",
]
#all colors:
COLORS = [
	pygame.Color(255,255,255), #WHITE
	pygame.Color(0,0,0), #BLACK
	pygame.Color(255,0,0), #RED
	pygame.Color(0,255,0), #GREEN
	pygame.Color(0,0,255), #BLUE
	pygame.Color(97,221,255), #BLUE SKY
	pygame.Color(255,0,160), #PINK
	pygame.Color(255,90,0), #ORANGE
	pygame.Color(255,255,0), #YELLOW
	pygame.Color(190,0,255), #PURPLE
	pygame.Color(120,120,120), #GREY
]


niveau = Niveau(LEVELS[0],WORLD_IMG)
niveau.read()
niveau.afficher()

up = down = left = right = running = False

joueur = Player(50,50,niveau.taille_sprite)

background_color = pygame.Surface((DISPLAY))
background_color.fill(COLORS[5])

while_bool = True

total_level_width  = len(niveau.structure[0])*niveau.taille_sprite
total_level_height = len(niveau.structure)*niveau.taille_sprite
camera = Camera(complex_camera, total_level_width, total_level_height)


#Main game loop
while while_bool:
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		if event.type == KEYDOWN:
			if event.key == K_RIGHT:
				right = True
			if event.key == K_LEFT:
				left = True
			if event.key == K_UP:
				up = True
			if event.key == K_DOWN:
				down = True
		elif event.type == KEYUP:
			if event.key == K_RIGHT:
				right = False
			if event.key == K_LEFT:
				left = False
			if event.key == K_UP:
				up = False
			if event.key == K_DOWN:
				down = False
	
	window.blit(background_color,(0,0))
	
	camera.update(joueur)
	joueur.update(up,down,left,right,running,niveau.world_block)
	
	for b in niveau.world_block:
		window.blit(b.image,camera.apply(b))
	window.blit(joueur.image,camera.apply(joueur))
	
	pygame.display.update()
	clock.tick(60)
