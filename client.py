import pygame, threading, socket
from pygame.locals import *

#Initialize the client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 5050))

#Initialize pygame
pygame.init()

display = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()

#Constants
RED = (255, 0, 0)
GREEN = (0, 255, 0)

class Player(object):
      def __init__(self, x, y, width, height):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.jumping = False
            self.jump_count = 10
            self.bottom = False
            self.top = False
            self.right = False
            self.left = False

      def jump(self):
            #Code used to make player jump
            if self.jump_count >= -10:
                  self.y -= (self.jump_count * abs(self.jump_count)) * 0.5
                  self.jump_count -= 1
            else: 
                  self.jump_count = 10
                  self.jumping = False

      def move(self):
            #Code used to handle player movement
            keys = pygame.key.get_pressed()

            if keys[pygame.K_a]:  
                  self.x -= 10

            if keys[pygame.K_d]:
                  self.x += 10

            if not self.jumping:
                  if keys[pygame.K_SPACE]:
                        self.jumping = True
            else:
                  self.jump()

            client.send(bytes(str(str(self.x) + "," + str(self.y) + "," + str(50) + "," + str(50)).encode()))


      def draw(self):
            pygame.draw.rect(display, RED, (self.x, self.y, self.width, self.height))

            self.move()

player = Player(560, 550, 50, 50)

def draw_game_window():
      #All code for drawing objects to the screen
      display.fill((0,0,0))

      data = client.recv(6000).decode()
      line = data

      try:
          pygame.draw.rect(display, GREEN, (float(line.split(",")[0]), float(line.split(",")[1]), 50, 50))
      except Exception as e:
          print(e)


      player.draw()

      
      pygame.display.update()
      clock.tick(60)

while True:
      #Main Loop

      draw_game_window()
      
      for event in pygame.event.get():
            if event == pygame.QUIT:
                  pygame.QUIT
                  quit()


