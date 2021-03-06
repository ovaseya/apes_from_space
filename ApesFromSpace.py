import pygame
import os
import random
import math
import time
from pygame import mixer
from pygame.locals import *
from pygame.compat import geterror


main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'data')

#Initilaizing Pygame
pygame.init()

clock = pygame.time.Clock()
#programming screen
screen = pygame.display.set_mode((1024, 576))
#Background
main_background = pygame.image.load('DeathStar.jpg')
#List of alternating menu Backgrounds
menu_background = pygame.image.load('menu_background.jpg')
#unused code for furture update
# menu_backgrounds = []
# menu_backgrounds.append(pygame.image.load('menu_background1.jpg'))
# menu_backgrounds.append(pygame.image.load('menu_background2.jpg'))
# menu_backgrounds.append(pygame.image.load('menu_background3.jpg'))
# menu_backgrounds.append(pygame.image.load('menu_background4.jpg'))
# menu_backgrounds.append(pygame.image.load('menu_background5.jpg'))
# menu_backgrounds.append(pygame.image.load('menu_background6.jpg'))
# menu_backgrounds.append(pygame.image.load('menu_background7.jpg'))
# menu_backgrounds.append(pygame.image.load('menu_background8.jpg'))
# menu_backgrounds.append(pygame.image.load('menu_background9.jpg'))
score_background = pygame.image.load('score_screen.jpg')


#Background music
mixer.music.load('MainMenuBGM.wav')
mixer.music.play(-1)

speed_up = mixer.Sound('speed_up.wav')


#title and icon of window
pygame.display.set_caption("APES FROM SPACE")
icon = pygame.image.load('monkey.png')
pygame.display.set_icon(icon)

#the enemy apes
ape1 = pygame.image.load('gorilla.png')
ape2 = pygame.image.load('monkeyTailed.png')
ape3 = pygame.image.load('baboon.png')
ape4 = pygame.image.load('spaceMonkey.png')
ape5 = pygame.image.load('monkeyBanana.png')
ape6 = pygame.image.load('monkeyBar.png')
ape7 = pygame.image.load('gorillaBlush.png')

enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
enemyIMG = []
enemyX_change_pixels = 0.6
enemyY_change_pixels = 40
apes_list = [ape1, ape2, ape3, ape4, ape5, ape6, ape7]

for ape in apes_list:
	enemyIMG.append(ape)
	enemyY.append(random.randint(0,100))
	enemyX.append(random.randint(0,1000))
	enemyX_change.append(enemyX_change_pixels)
	enemyY_change.append(enemyY_change_pixels)


#da banana ooh ooh aah aah
#banana state: states of banana represented as string, they determine what the banana will do
#banana states: "unseen"=banana is not animated and cannot be seen, "fire": banana is fired
bananaIMG = pygame.image.load('banana.png')
bananaX = 0
bananaY = 490
bananaX_change = 0
bananaY_change = 4
banana_state = "unseen"

#score information
score_value = 0
bananas = 0
score_text = "Score "
score_difficulties = [20, 40, 60, 80]

#font information
font = pygame.font.Font('8-BIT WONDER.ttf', 16)
game_overfont = pygame.font.Font('8-BIT WONDER.ttf', 32)
pause_font = pygame.font.Font('8-BIT WONDER.ttf', 32)
menu_font = pygame.font.Font('8-BIT WONDER.ttf', 64)
directions_font = pygame.font.Font('8-BIT WONDER.ttf', 32)
textX = 10
textY = 10

def show_score(x, y):
	score = font.render(score_text + str(score_value), True, (0, 255, 0) )
	screen.blit(score, (x, y))
	banan = font.render('Bananas ' + str(bananas), True, (255, 255, 0) )
	screen.blit(banan, (x, y+15))

def game_over_text():
	game_over_text = game_overfont.render('Game Over', True, (255, 0, 0))
	screen.blit(game_over_text, (360, 235))

def menu_text():
	menu_text = menu_font.render("APES FROM SPACE", True, (100,200,99))
	directions_text = directions_font.render("Click To Begin", True, (255,100,100))
	credits_text = font.render("Created by Jared Keklak Python - 236", True, (255, 255, 0))
	screen.blit(menu_text, (50, 100))
	screen.blit(credits_text, (250, 200))
	screen.blit(directions_text, (320, 500))


def you_win_text():
	win_text = menu_font.render("YOU WON", True, (0, 255, 100))
	msg_text = directions_font.render("YOU DEFEATED THE ENEMY APE FLEET", True, (0, 255, 100))
	directions_text = font.render("click once to continue", True, (255, 100, 0))
	screen.blit(win_text, (275, 100))
	screen.blit(msg_text, (25, 350))
	screen.blit(directions_text, (350, 450))

def score_screen_text():
	difference = bananas - score_value
	score_summary = directions_font.render("Apes Defeated " + str(score_value), True, (0, 255, 0))
	banana_summary = directions_font.render("Bananas Fired " + str(bananas), True, (255, 255, 0))
	ratio_summary = directions_font.render("Misses " + str(difference), True, (255, 0, 255))
	message = font.render("Thanks for playing Click to exit", True, (0, 255, 0))
	screen.blit(score_summary, (300, 200))
	screen.blit(banana_summary, (300, 250))
	screen.blit(ratio_summary, (300, 300))
	screen.blit(message, (270, 500))


def pause():
	paused = True
	while paused:
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_c:
					paused = False
				elif event.key == pygame.K_q:
					pygame.quit()
		Paused_text = pause_font.render("Paused", True, (0, 0, 0))
		Paused_msg = pause_font.render("Press C to continue or Q to quit", True, (0, 0, 0))
		screen.blit(Paused_text, (400, 150))
		screen.blit(Paused_msg, (80, 500))
		pygame.display.update()
		clock.tick(10)
		
#method for blitting player battleship to screen
def player(x, y):
	screen.blit(spaceshipIMG, (x, y))
#method for blitting enemy apes to screen
def enemy(IMG, x, y):
	screen.blit(IMG, (x, y))
#method to fire banana
def fire_banana(x, y):
	global banana_state
	banana_state = "fire"
	screen.blit(bananaIMG, (x, y + 10))
#method that calculates collision or banana and ape
#uses the distance formula for 2 xy coordinates
def isCollision(apeX, apeY, bananaX, bananaY):
	distance = math.sqrt(math.pow(apeX - bananaX, 2) + math.pow(apeY - bananaY, 2))
	if distance < 27:
		return True
	else:
		return False
	


def load_image(name, colorkey=None):
	try:
		image = pygame.image.load(name)
	except pygame.error:
		print ('Cannot load image:', fullname)
		raise SystemExit(str(geterror()))
	image = image.convert()
	if colorkey is not None:
		if colorkey == -1:
			colorkey = image.get_at((0,0))
		image.set_colorkey(colorkey, RLEACCEL)
	return image, image.get_rect()

#classes for our game objects
class Spaceship(pygame.sprite.Sprite):
	"""moves a spaceship on the screen, following the mouse"""
	def __init__(self):
		pygame.sprite.Sprite.__init__(self) #call Sprite initializer
		self.image, self.rect = load_image('battleship.png', -1)
		

	def update(self):
		"move the spaceship based on the mouse position"
		pygame.mouse.set_visible(False)
		pos = pygame.mouse.get_pos()
		self.rect.midtop = pos
		if pos[1] != 490:
			pygame.mouse.set_pos(pos[0], 490)


#the game loop
ship = Spaceship()
allsprites = pygame.sprite.RenderPlain(ship)
going = True
menu = True
won = False
score_screen = False
speedUp1 = True
speedUp2 = True
speedUp3 = True
speedUp4 = True
while going:


	while(menu):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				going = False
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					menu = False
					mixer.music.unload()
					mixer.music.load('ElectronicBGM.wav')
					mixer.music.play(-1)
					

		screen.fill((0,0,0))
		clock.tick(30)
		# for background in menu_backgrounds:
		# 	screen.blit(background, (0,0))
		# 	menu_text()
		# 	clock.tick(2)
		# 	pygame.display.update()

		screen.blit(menu_background, (0,0))
		menu_text()
		pygame.display.update()

	screen.fill((0,0,0))
	#background image load
	screen.blit(main_background, (0,0))
	



	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			going = False
		elif event.type == KEYDOWN and event.key == K_ESCAPE:
			going = False
		elif event.type == KEYDOWN and event.key == K_p:
			mixer.music.stop()
			pause()
			mixer.music.play(-1)
		if event.type == pygame.MOUSEBUTTONDOWN:
			#when button is pressed, banana is only fired if it is "unseen" meaning not already on the screen
			if banana_state == "unseen":
				banana_sound = mixer.Sound('Gun-laser-sound.wav')
				banana_sound.play()
				#bullet is fired from current mouse positon
				bananaX = pygame.mouse.get_pos()[0]
				fire_banana(bananaX, bananaY)
				bananas += 1

	allsprites.update()
	allsprites.draw(screen)	

	#Boudaries and movement for enemy apes
	for i in range(len(apes_list)):
		#game over code
		if enemyY[i] > 450:
			for j in range(len(apes_list)):
				enemyY[j] = 2000
			mixer.music.stop()
			game_over_text()
			ape_cheer = mixer.Sound('monkey4.wav')
			ape_cheer.play()
			for event in pygame.event.get():
				if event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 1:
						score_screen = True
			break

		enemyX[i] += enemyX_change[i]
		if enemyX[i] <= 0:
			enemyX_change[i] =  enemyX_change_pixels
			enemyY[i] += enemyY_change[i]
		elif enemyX[i] >= 980:
			enemyX_change[i] = -(enemyX_change_pixels)
			enemyY[i] += enemyY_change[i]

		#ape and banana collision
		collision = isCollision(enemyX[i], enemyY[i], bananaX, bananaY)
		if collision:
			monkey_sound = mixer.Sound('woow_x.wav')
			monkey_sound.play()
			bananaY = 490
			score_value += 1
			banana_state = "unseen"
			enemyY[i] = random.randint(1, 50)
			enemyX[i] = random.randint(1,1000)

		
		enemy(apes_list[i], enemyX[i], enemyY[i])

	#banana movement
	if bananaY <=0:
		bananaY = 490
		banana_state = "unseen"
	if banana_state == "fire":
		fire_banana(bananaX, bananaY)
		bananaY -= bananaY_change

	#difficulty levels, apes get faster after each score standard.
	if (score_value == 15):
		if(speedUp1):
			mixer.music.stop()
			speed_up.play()
			mixer.music.play(-1)
			speedUp = False
		for i in range(len(apes_list)):
			enemyX_change_pixels = 0.9

	if (score_value == 30):
		if(speedUp2):
			mixer.music.stop()
			speed_up.play()
			mixer.music.play(-1)
			speedUp2 = False
		for i in range(len(apes_list)):
			enemyX_change_pixels = 1.1
			

	if (score_value == 45):
		if(speedUp3):
			mixer.music.stop()
			speed_up.play()
			mixer.music.play(-1)
			speedUp3 = False
		for i in range(len(apes_list)):
			enemyX_change_pixels = 1.4
			

	if (score_value == 60):
		won = True

	while(won):

	


		for i in range(len(apes_list)):
			enemyY_change[i] = -100
			enemyX_change[i] = 2
			
		mixer.music.unload()
		enemyY_change_pixels = 0
		won_cheer = mixer.Sound('monkeyclip5.wav')
		won_cheer.play()
		you_win_text()
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:
				#if event.button == 1:
				won = False
				score_screen = True
				won_cheer.stop()
				mixer.music.unload()
				mixer.music.load('RE2OST_endingTheme.wav')
				mixer.music.play(-1)
				




		break
		

	while(score_screen):
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					score_screen = False
					going = False

		screen.fill((0,0,0))
		screen.blit(score_background, (0,0))
		score_screen_text()
		clock.tick(30)
		pygame.display.update()
		
		



	show_score(textX, textY)
	pygame.display.update()

