import pygame
import numpy


pygame.init()
gameDisplay = pygame.display.set_mode((800,600))
pygame.display.set_caption('Race car')
clock = pygame.time.Clock() #clock vai ser os frames que a gente vai colocar no jogo

crashed = False

while not crashed:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

        print(event)

    pygame.display.update() #essa função atualiza somente alguns locais da tela, a que atualiza toda a tela é display.flip()
    clock.tick(60)
