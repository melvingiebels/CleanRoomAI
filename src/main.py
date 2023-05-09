import pygame
import sys
from room_generation import generate_room, draw_room
from robot_simulation import bfs, dfs, a_star
from button import Button

pygame.init()
window_size = (800, 600)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("My Living Room")

room, robot_position = generate_room((0, 0))

font = pygame.font.Font(None, 36)

# Create buttons for the different search algorithms
dfs_button = Button(650, 10, 120, 40, "Run DFS", (0, 128, 0), (255, 255, 255), 24)
bfs_button = Button(650, 60, 120, 40, "Run BFS", (0, 0, 128), (255, 255, 255), 24)
astar_button = Button(650, 110, 120, 40, "Run A*", (255, 255, 0), (0, 0, 0), 24)

timer = pygame.time.Clock()
fps = 60

# Add a variable to keep track of the chosen algorithm
chosen_algorithm = None

while True:
    timer.tick(fps)
    dfs_button.draw(screen)
    bfs_button.draw(screen)
    astar_button.draw(screen)
    draw_room(screen, room, robot_position, font, steps=0)
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
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            # Check if the user clicked on a tile
            robot_position = pygame.mouse.get_pos()
            # convert the position to the tile position
            robot_position = (robot_position[0] // 50, robot_position[1] // 50)
            draw_room(screen, room, robot_position, font, steps=0)
            pygame.display.update()
        elif dfs_button.is_clicked(event):
            dfs(screen, font, robot_position, room, set(), steps=0)
        elif bfs_button.is_clicked(event):
            bfs(screen, font, robot_position, room)
        elif astar_button.is_clicked(event):
            a_star(screen, font, robot_position, room)

        # elif dfs_button.is_clicked(event):
        #     dfs(screen, font, robot_position, room, set(), steps=0)
        #     pygame.display.update()
        # elif bfs_button.is_clicked(event):
        #     bfs(screen, font, robot_position, room)
        #     pygame.display.update()
        # elif event.type == pygame.MOUSEBUTTONDOWN:
        #     # Check if the user clicked on a tile
        #     robot_position = pygame.mouse.get_pos()
        #     #convert the position to the tile position
        #     robot_position = (robot_position[0] // 50, robot_position[1] // 50)
        #     draw_room(screen, room, robot_position, font, steps=0)
        #     a_star(screen, font, robot_position, room)
        #     pygame.display.update()
