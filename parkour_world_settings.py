import pygame, sys, os, random
from pygame.locals import *

pygame.init()

WIN_WIDTH = 800
WIN_HEIGHT = 640
HALF_WIDTH = int(WIN_WIDTH / 2)
HALF_HEIGHT = int(WIN_HEIGHT / 2)

DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
DEPTH = 32
FLAGS = 0
CAMERA_SLACK = 30

#all textures about the environment:
BLOCK_IMG = [
	pygame.transform.scale(pygame.image.load("Data/Pictures/world_textures/grass.png"),(25,25)),#GRASS
	pygame.transform.scale(pygame.image.load("Data/Pictures/world_textures/dirt.png"),(25,25)),#DIRT
	pygame.transform.scale(pygame.image.load("Data/Pictures/world_textures/stone.png"),(25,25)),#STONE
	pygame.transform.scale(pygame.image.load("Data/Pictures/world_textures/brick.png"),(25,25)),#BRICK
	pygame.transform.scale(pygame.image.load("Data/Pictures/world_textures/coin.png"),(25,25)),#COIN
	pygame.transform.scale(pygame.image.load("Data/Pictures/world_textures/lava.png"),(25,25)),#LAVA
]
BG_BLOCK_IMG = [
	pygame.transform.scale(pygame.image.load("Data/Pictures/world_textures/bg_grass.png"),(25,25)),#BG GRASS
	pygame.transform.scale(pygame.image.load("Data/Pictures/world_textures/bg_dirt.png"),(25,25)),#BG DIRT
	pygame.transform.scale(pygame.image.load("Data/Pictures/world_textures/bg_stone.png"),(25,25)),#BG STONE
	pygame.transform.scale(pygame.image.load("Data/Pictures/world_textures/bg_brick.png"),(25,25)),#BG BRICK
	pygame.transform.scale(pygame.image.load("Data/Pictures/world_textures/bg_coin.png"),(25,25)),#BG COIN
	pygame.transform.scale(pygame.image.load("Data/Pictures/world_textures/bg_lava.png"),(25,25)),#BG LAVA
]

#level file base name
LEVEL = "LEVELS/parkour_world_lvl"
BACKGROUND_LEVEL = "LEVELS/BG/parkour_background_world_lvl"

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
	pygame.Color(120,120,120,10), #DARK
]

#all FONTS
FONTS = [
	pygame.font.SysFont("arial",35),
]


up = down = left = right = running = False

while_bool = True
