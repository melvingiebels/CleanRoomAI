import random
import pygame
import sys
from room_generation import generate_room, draw_room, generate_and_draw_room, clean_current_room
from robot_simulation import bfs, dfs, a_star, pattern_cleaning, random_cleaning
from button import Button

pygame.init()
window_size = (800, 600)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("My Living Room")

font = pygame.font.Font(None, 36)

room, robot_position = generate_and_draw_room(screen, font)

# Create buttons for the different search algorithms
room_button = Button(440, 10, 120, 40, "New room", (128, 128, 128), (255, 255, 255), 24)
clean_room_button = Button(440, 60, 120, 40, "Clean room", (128, 128, 128), (255, 255, 255), 24)
dfs_button = Button(440, 110, 120, 40, "Run DFS", (0, 128, 0), (255, 255, 255), 24)
bfs_button = Button(440, 160, 120, 40, "Run BFS", (0, 0, 128), (255, 255, 255), 24)
astar_button = Button(440, 210, 120, 40, "Run A*", (255, 255, 0), (0, 0, 0), 24)
random_button = Button(440, 260, 120, 40, "Run Random", (255, 255, 128), (0, 0, 0), 24)
random_bulk_button = Button(440, 310, 120, 40, "Run RandomX3", (128, 255, 128), (0, 0, 0), 24)

while True:
    room_button.draw(screen)
    clean_room_button.draw(screen)
    dfs_button.draw(screen)
    bfs_button.draw(screen)
    astar_button.draw(screen)
    random_button.draw(screen)
    random_bulk_button.draw(screen)

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
        elif room_button.is_clicked(event):
            room, robot_position = generate_and_draw_room(screen, font)
        elif clean_room_button.is_clicked(event):
            clean_current_room(screen, font, room)
        elif dfs_button.is_clicked(event):
            dfs(screen, font, robot_position, room, set(), steps=0)
        elif bfs_button.is_clicked(event):
            bfs(screen, font, robot_position, room)
        elif astar_button.is_clicked(event):
            a_star(screen, font, robot_position, room)
        elif random_button.is_clicked(event):
            robot_position, moves = pattern_cleaning(screen, font, robot_position, room, True)
        elif random_bulk_button.is_clicked(event):
            num_rooms = 1000
            total_path_length = 0
            for i in range(num_rooms):
                pygame.event.get()  # Add this line to prevent the window from freezing
                print(f"New room {i + 1}")

                # Make new room
                while True:
                    room, robot_position = generate_and_draw_room(screen, font)

                    # Start cleaning
                    result = random_cleaning(screen, font, robot_position, room, False)
                    if result is not None:
                        robot_position, path_length = result
                        break

                total_path_length += path_length
                print(f"Total now is: {total_path_length:.2f}")
                average_path_length = total_path_length / 1000
            print(f"Random movement average path length: {average_path_length:.2f}")

    pygame.display.update()
