from pygame import *
# from random import randint as r

WIDTH = 800
HEIGHT = 600
size=(WIDTH, HEIGHT)
screen = display.set_mode(size) 
key.set_repeat(10,10)
font.init()
timesNewRomanFont = font.SysFont("Times New Roman", 24)
myClock = time.Clock()

player = Rect(0, 0, 100, 100)

running = True
while running:
    for evt in event.get():
        if evt.type == QUIT:
            running = False
        if evt.type == KEYDOWN:
            if evt.key == K_ESCAPE:
                running = False

    mx, my = mouse.get_pos()
    mb = mouse.get_pressed()
    kp = key.get_pressed()

    if kp[K_DOWN]:
        player = player.move(0, 1)

    draw.rect(screen, (255, 0, 0), player)
    display.flip()

quit()
