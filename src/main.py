import random
import pygame
import sys
from room_generation import generate_room, draw_room, generate_and_draw_room
from robot_simulation import bfs, dfs, a_star, random_cleaning
from button import Button

pygame.init()
window_size = (800, 600)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("My Living Room")

font = pygame.font.Font(None, 36)

# room, robot_position = generate_and_draw_room(screen, font)

# Create buttons for the different search algorithms
# room_button = Button(440, 10, 120, 40, "New room", (128, 128, 128), (255, 255, 255), 24)
# dfs_button = Button(440, 60, 120, 40, "Run DFS", (0, 128, 0), (255, 255, 255), 24)
# bfs_button = Button(440, 110, 120, 40, "Run BFS", (0, 0, 128), (255, 255, 255), 24)
# astar_button = Button(440, 160, 120, 40, "Run A*", (255, 255, 0), (0, 0, 0), 24)
# random_button = Button(440, 210, 120, 40, "Run Random", (255, 255, 128), (0, 0, 0), 24)
# random_bulk_button = Button(
#     440, 260, 120, 40, "Run RandomX3", (128, 255, 128), (0, 0, 0), 24
# )

random_clean_button_counter = 0
total_path_length = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if random_clean_button_counter < 1000:
        print(f"New room {random_clean_button_counter + 1}")

        # Make new room
        while True:
            room, robot_position = generate_and_draw_room(screen, font)

            # Start cleaning
            result = random_cleaning(screen, font, robot_position, room)
            if result is not None:
                robot_position, path_length = result
                break

        total_path_length += path_length
        random_clean_button_counter += 1
        print(f"Total now is: {total_path_length:.2f}")
        average_path_length = total_path_length / 1000
        print(f"Random movement average path length: {average_path_length:.2f}")

    # Draw room
    # draw_room(screen, room, robot_position, font, steps=0)
    # pygame.display.update()
