import pygame, sys, os, random
from pygame.locals import *
from parkour_world_class import *
from parkour_world_settings import *

pygame.init()

window = pygame.display.set_mode(DISPLAY, FLAGS, DEPTH)
clock = pygame.time.Clock()


joueur = Player(50,600,25,25)

niveau = WorldManager(BLOCK_IMG,BG_BLOCK_IMG)
niveau.generate(LEVEL+str(niveau.level),BACKGROUND_LEVEL+str(niveau.level))

total_level_width  = len(niveau.structure[0])*niveau.taille_sprite
total_level_height = len(niveau.structure)*niveau.taille_sprite
camera = Camera(complex_camera, total_level_width, total_level_height)

background_color = pygame.Surface((DISPLAY))
background_color.fill(COLORS[5])

hud = HUD(WIN_WIDTH, WIN_HEIGHT, window, FONTS[0])


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
			if event.key == K_SPACE:
				running = True
		elif event.type == KEYUP:
			if event.key == K_RIGHT:
				right = False
			if event.key == K_LEFT:
				left = False
			if event.key == K_UP:
				up = False
			if event.key == K_DOWN:
				down = False
			if event.key == K_SPACE:
				running = False
	
	window.blit(background_color,(0,0))
	
	camera.update(joueur)
	niveau.update(joueur)
	joueur.update(up,down,left,right,running,niveau.try_collide,niveau.world_block)
	
	for bb in niveau.world_background_block:
		window.blit(bb.image,camera.apply(bb))
	
	window.blit(joueur.image,camera.apply(joueur))
	
	for b in niveau.world_block:
		window.blit(b.image,camera.apply(b))
	
	hud.coins(joueur.coins,COLORS[0],BLOCK_IMG[4])
	hud.health_bar(COLORS[2],COLORS[3],joueur.hp,joueur.max_hp)
	hud.mana_bar(COLORS[2],COLORS[4],joueur.mana,joueur.max_mana)
	
	pygame.display.update()
	clock.tick(60)
