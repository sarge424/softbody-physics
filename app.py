from vector import Vector
from body import Body

import math

import pygame
pygame.init()
pygame.font.init()

FPS = 100
WIDTH = 500
HEIGHT = 500
MARGINS = 50

n = 50
b1 = Body(n, n, verts=False, fill=False, forces=False)
b1.generate_points(50, Vector(200, 200), -90 + 360/n)
b1.generate_edges([(x, x+1) for x in range(-1, n-1)])
b1.add_force(Vector(0,0))

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Blob')

def update_game():
    screen.fill((200,200,200))
    WIDTH, HEIGHT = screen.get_size()
    b1.move((MARGINS, MARGINS, WIDTH-MARGINS, HEIGHT-MARGINS))
    b1.draw(screen)
    pygame.display.flip()

run = True
paused = True
clock = pygame.time.Clock()
while run:
	clock.tick(FPS) #FPS
	update_game()

	for event in pygame.event.get():
		if event.type == pygame.QUIT: #pressed the 'X'
			run = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				paused = not paused
			if event.key == pygame.K_UP:
				b1.add_force(Vector(0,-1))
			if event.key == pygame.K_LEFT:
				b1.add_force(Vector(-1,0))
			if event.key == pygame.K_DOWN:
				b1.add_force(Vector(0,1))
			if event.key == pygame.K_RIGHT:
				b1.add_force(Vector(1,0))
			if event.key == pygame.K_x:
				b1.add_force(Vector(0,0))
		if event.type == pygame.MOUSEBUTTONUP:
				b1.add_force(Vector())
    
	if pygame.mouse.get_pressed()[0]:
		b1.add_force(Vector.from_tuple(pygame.mouse.get_pos()) - Vector.average(b1.pos))