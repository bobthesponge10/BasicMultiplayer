import pygame
import math
import socket

ready = False
ready1 = 0

pygame.init()

clock = pygame.time.Clock()
done = False

s = socket.socket()
host = socket.gethostname()
port = 10000
connect = input("Connect to: ")
s.connect((connect, port))

while not ready:
    print(ready1)
    ready1 = int(s.recv(1024))
    if ready1 == 1:
        ready = True


Fullscreen = 0
Screensize = (pygame.display.Info().current_w, pygame.display.Info().current_h)
screen = pygame.display.set_mode(Screensize, pygame.FULLSCREEN)
screen = pygame.display.set_mode(Screensize)
pygame.mouse.set_visible(False)

PI = math.pi

Walls = [[0, 0, 20, Screensize[1], (0, 255, 0)],
         [0, 0, Screensize[0], 20, (0, 255, 0)],
         [Screensize[0]-20, 0, 20, Screensize[1], (0, 255, 0)],
         [0, Screensize[1]-20, Screensize[0], 20, (0, 255, 0)]


         ]

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()

        self.xSpeed = 0
        self.ySpeed = 0
        self.image = pygame.Surface([20, 20])
        self.rect = self.image.get_rect()
        self.image.fill(color)
        self.rect.x = x
        self.rect.y = y

    def speedchange(self, x ,y):
        self.xSpeed += x
        self.ySpeed += y

    def update(self):
        self.rect.x += self.xSpeed
        block_hit_list = pygame.sprite.spritecollide(self, walls, False)
        for i in block_hit_list:
            if self.xSpeed > 0:
                self.rect.right = i.rect.left
            else:
                self.rect.left = i.rect.right

        self.rect.y += self.ySpeed
        block_hit_list = pygame.sprite.spritecollide(self, walls, False)
        for i in block_hit_list:
            if self.ySpeed > 0:
                self.rect.bottom = i.rect.top
            else:
                self.rect.top = i.rect.bottom


walls = pygame.sprite.Group()
players = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

player2 = Wall(400, 400, 20, 20, (255, 0, 0))
walls.add(player2)
all_sprites.add(player2)


player = Player(200, 200, (0, 0, 255))
players.add(player)
all_sprites.add(player)

player.rect.x = int(s.recv(1024))
s.send(b"1")
player.rect.x = int(s.recv(1024))
s.send(b"1")

for i in Walls:
    wall = Wall(i[0], i[1], i[2], i[3], i[4])
    walls.add(wall)
    all_sprites.add(wall)

print("bob")
while not done:
    player2.rect.x = int(s.recv(1024))
    s.send(str(player.rect.x).encode())
    player2.rect.y = int(s.recv(1024))
    s.send(str(player.rect.y).encode())
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == 27:
                done = True
            if event.key == pygame.K_LEFT:
                player.speedchange(-3, 0)
            elif event.key == pygame.K_RIGHT:
                player.speedchange(3, 0)
            elif event.key == pygame.K_UP:
                player.speedchange(0, -3)
            elif event.key == pygame.K_DOWN:
                player.speedchange(0, 3)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_f:
                if Fullscreen == 1:
                    pygame.display.set_mode(Screensize)
                    pygame.mouse.set_visible(True)
                    Fullscreen = 0
                else:
                    pygame.display.set_mode(Screensize, pygame.FULLSCREEN)
                    pygame.mouse.set_visible(False)
                    Fullscreen = 1

            if event.key == pygame.K_LEFT:
                player.speedchange(3, 0)
            elif event.key == pygame.K_RIGHT:
                player.speedchange(-3, 0)
            elif event.key == pygame.K_UP:
                player.speedchange(0, 3)
            elif event.key == pygame.K_DOWN:
                player.speedchange(0, -3)

    screen.fill((255, 255, 255))






    players.update()
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(60)
s.close
pygame.quit()
