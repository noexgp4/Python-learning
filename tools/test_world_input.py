import sys
sys.path.append(r'e:/Python learning/Python-learning/Python-learning')
import pygame
from Scenes.world_scene import WorldScene

pygame.init()
screen = pygame.display.set_mode((100, 100))
ws = WorldScene(screen)

evt_b = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_b})
evt_space = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_SPACE})
evt_a = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_a})

print('K_b ->', ws.handle_input(evt_b))
print('K_SPACE ->', ws.handle_input(evt_space))
print('K_a ->', ws.handle_input(evt_a))

pygame.quit()
