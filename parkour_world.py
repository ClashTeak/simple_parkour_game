import pygame, sys, os, random
from pygame.locals import *
from parkour_world_class import *

pygame.init()

xWmax = 800
yWmax  = 600
window = pygame.display.set_mode((xWmax,yWmax))
clock = pygame.time.Clock()

WORLD_IMG = [
	pygame.image.load("Data/Pictures/world_textures/grass.png"),#HERBE
	pygame.image.load("Data/Pictures/world_textures/dirt.png"),#TERRE
	pygame.image.load("Data/Pictures/world_textures/stone.png"),#PIERRE
]
PLAYER_IMG = [
	pygame.image.load("Data/Pictures/Player/player.png")#IDLE
]
LEVELS = [
	"parkour_world_lvl1",
	"parkour_world_lvl2",
	"parkour_world_lvl3",
	"parkour_world_lvl4",
	"parkour_world_lvl5",
]
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

niveau = Niveau(LEVELS[0],WORLD_IMG[0],WORLD_IMG[1],WORLD_IMG[2])
physics = Physics()

All_object = [Joueur(400,250,PLAYER_IMG[0])]

background_color = pygame.Surface((xWmax,yWmax))
world_surface = pygame.Surface((xWmax,yWmax))
background_color.fill(COLORS[5])

while_bool = True

niveau.read()
world_surface.blit(background_color,(0,0))
niveau.afficher(world_surface)

while while_bool:
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
	
	physics.onGravity(All_object)
	All_object[0].update()
	window.blit(world_surface,(0,0))
	All_object[0].draw(window)
	pygame.display.update()
	clock.tick(60)
