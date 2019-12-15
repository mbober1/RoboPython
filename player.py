import os
import sys
import vlc
import pygame
import random, time

white = (255, 255, 255) 
black = (0, 0, 0) 
ping=0
	
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((800,600),pygame.RESIZABLE)
pygame.display.get_wm_info()
pygame.display.set_caption('Player3000')

font = pygame.font.Font('freesansbold.ttf', 11)
text = font.render('Ping: ' + str(ping) + 'ms', True, white, black)
textRect = text.get_rect() 
textRect.center = (760, 10) 




# print("Using %s renderer" % pygame.display.get_driver())

vlcInstance = vlc.Instance()
media = vlcInstance.media_new('http://192.168.0.206:12345/stream.mjpg')

# Create new instance of vlc player
player = vlcInstance.media_player_new()
# Pass pygame window id to vlc player, so it can render its contents there.
player.set_hwnd(pygame.display.get_wm_info()['window'])
# Load movie into vlc player instance
player.set_media(media)

# Quit pygame mixer to allow vlc full access to audio device (REINIT AFTER MOVIE PLAYBACK IS FINISHED!)
pygame.mixer.quit()

# Start movie playback
player.play()	
pos=(100,100)

game_surf = pygame.surface.Surface(pos)
game_surf.fill(white)

while player.get_state() != vlc.State.Ended:
	ping = random.randint(0, 5)
	text = font.render('Ping: ' + str(ping) + 'ms', True, white, black)

	pygame.display.update() 
	

	for event in pygame.event.get():
		
		if event.type == pygame.QUIT:
			sys.exit(2)
