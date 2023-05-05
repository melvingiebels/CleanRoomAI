import pygame
import sys
from room_generation import generate_room, draw_room
from robot_simulation import dfs
from button import Button

pygame.init()
window_size = (800, 600)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("My Living Room")

room, robot_position = generate_room()

font = pygame.font.Font(None, 36)

# Create buttons for the different search algorithms
dfs_button = Button(650, 10, 120, 40, "Run DFS", (0, 128, 0), (255, 255, 255), 24)
bfs_button = Button(650, 60, 120, 40, "Run BFS", (0, 0, 128), (255, 255, 255), 24)

timer = pygame.time.Clock()
fps = 60

while True:
    timer.tick(fps)
    dfs_button.draw(screen)
    bfs_button.draw(screen)
    mouse_pos = pygame.mouse.get_pos()
    pygame.display.update()

    if dfs_button.is_hovered(mouse_pos) or bfs_button.is_hovered(mouse_pos):
        pygame.mouse.set_cursor(*pygame.cursors.diamond)
    else:
        pygame.mouse.set_cursor(*pygame.cursors.arrow)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif dfs_button.is_clicked(event):
            dfs(screen, font, robot_position, room, set())
            pygame.display.update()
        elif bfs_button.is_clicked(event):
            dfs(screen, font, robot_position, room, set())
            pygame.display.update()
