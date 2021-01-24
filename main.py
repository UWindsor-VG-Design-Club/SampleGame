from pygame import *
from random import randint

WIDTH = 1024
HEIGHT = 1024
size=(WIDTH, HEIGHT)
screen = display.set_mode(size) 
key.set_repeat(10,10)
font.init()
timesNewRomanFont = font.SysFont("Times New Roman", 24)
myClock = time.Clock()

background = image.load("Assets/backgrounds/space-2.jpg").convert_alpha()
explosion = list()
for i in range(73):
    explosion.append(image.load(f"Assets/EXPLOSION/{i}.png").convert_alpha())

player = sprite.Group()
enemies = sprite.Group()
player_bullets = sprite.Group()
enemy_bullets = sprite.Group()

def create_enemies():
    for i in range(5):
        for j in range(11):
            tmp = Enemy()
            tmp.move_to(50 + tmp.rect.width * j + 20 * j, 50 + tmp.rect.height * i + 15 * i)
            enemies.add(tmp)

class Enemy(sprite.Sprite):
    def __init__(self):
        sprite.Sprite.__init__(self)
        self.image = transform.rotozoom(image.load("Assets/enemies/0.png").convert_alpha(), 180, 1)
        self.rect = self.image.get_rect()
        self.is_alive = True
        self.counter = self.frame = 0
        
    def update(self):
        if self.is_alive and len(sprite.spritecollide(self, player_bullets, True)) > 0:
            self.is_alive = False
            self.dead_rect = self.rect

        if not self.is_alive:
            self.counter += 1
            self.image = explosion[self.frame]
            self.rect = self.image.get_rect()
            self.rect.x = self.dead_rect.x + self.dead_rect.width / 2 - self.rect.width / 2
            self.rect.y = self.dead_rect.y + self.dead_rect.height / 2 - self.rect.height / 2
            if self.counter > 5:
                self.counter = 0
                self.frame += 1
                if self.frame >= len(explosion):
                    self.kill()

    def move_to(self, x, y):
        self.rect.x, self.rect.y = x, y

    def shoot(self):
        if len(enemy_bullets.sprites()) == 0 and self.is_alive:
            enemy_bullets.add(Bullet(self.rect.x + self.rect.width / 2 - 8, self.rect.y, False))

class Player(sprite.Sprite):
    def __init__(self):
        sprite.Sprite.__init__(self)
        self.image = transform.rotozoom(image.load("Assets/player.png").convert_alpha(), 90, 0.5)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = WIDTH / 2 - self.rect.width / 2, HEIGHT / 2 + 300
        self.last_shoot = 0
        
    def update(self):
        if kp[K_RIGHT] and self.rect.x + self.rect.width < WIDTH:
            self.rect.x += 5

        if kp[K_LEFT] and self.rect.x > 0:
            self.rect.x += -5

        if kp[K_SPACE] and len(player_bullets.sprites()) < 2 and time.get_ticks() - self.last_shoot > 500:
            player_bullets.add(Bullet(self.rect.x + self.rect.width / 2 - 8, self.rect.y, True))
            self.last_shoot = time.get_ticks()

        sprite.groupcollide(player, enemy_bullets, False, True)


class Bullet(sprite.Sprite):

    def __init__(self, x, y, is_player):
        sprite.Sprite.__init__(self)
        self.image = transform.rotozoom(image.load("Assets/bullet.png").convert_alpha(), 0 if is_player else 180, 1)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.is_player = is_player
        
    def update(self):
       self.rect.y -= 5 if self.is_player else -5 
       if self.rect.y < -self.rect.height or self.rect.y > HEIGHT + self.rect.height:
           self.kill()

player.add(Player())
create_enemies();
# enemies.add(Enemy(0, 0))

running = True
while running:
    for evt in event.get():
        if evt.type == QUIT:
            running = False
        if evt.type == KEYDOWN:
            if evt.key == K_q:
                running = False

    mx, my = mouse.get_pos()
    mb = mouse.get_pressed()
    kp = key.get_pressed()

    screen.blit(background, (0, 0))

    # UPDATING OBJECTS
    player.update()
    player_bullets.update()

    enemies.update()
    enemy_bullets.update()

    if len(enemies.sprites()) > 0:
        enemies.sprites()[randint(0, len(enemies.sprites()) - 1)].shoot()

    # DRAWING TO SCREEN
    player.draw(screen)
    player_bullets.draw(screen)

    enemies.draw(screen)
    enemy_bullets.draw(screen)
    

    display.flip()
    myClock.tick(120)
quit()
