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

niveau = Niveau(LEVELS[0],WORLD_IMG)
joueur = Joueur(420,250,PLAYER_IMG[0],0.2)


background_color = pygame.Surface((xWmax,yWmax))
background_color.fill(COLORS[5])

while_bool = True

niveau.read()
niveau.afficher()

while while_bool:
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		if event.type == KEYDOWN:
			if event.key == K_RIGHT:
				joueur.xs = 2
			if event.key == K_LEFT:
				joueur.xs = -2
			if event.key == K_UP:
				if joueur.have_gravity:
					joueur.jump()
				else:
					joueur.ys = -2
			if event.key == K_DOWN:
				if joueur.have_gravity == False:
					joueur.ys = 2
					
		elif event.type == KEYUP:
			if event.key == K_RIGHT or event.key == K_LEFT:
				joueur.xs = 0
			if event.key == K_UP or event.key == K_DOWN:
				if joueur.have_gravity == False:
					joueur.ys = 0
	
	
	joueur.update(niveau.print_block)
	
	window.blit(background_color,(0,0))
	niveau.update(joueur)
	for b in niveau.print_block:
		window.blit(b.image,b.rect)
	
	joueur.draw(window)
	
	pygame.display.update()
	clock.tick(60)
