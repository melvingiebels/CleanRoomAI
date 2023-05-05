import pygame
import sys
from room_generation import generate_room, draw_room
from robot_simulation import dfs

pygame.init()
window_size = (800, 600)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("My Living Room")

room, robot_position = generate_room()

font = pygame.font.Font(None, 36)

timer = pygame.time.Clock()
fps = 60

while True:
    timer.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Perform depth-first search
                dfs(screen, font, robot_position, room, set())
                pygame.display.update()
