import time
from room_generation import draw_room, room_width, room_height
import pygame

def dfs(screen, font, position, room, visited):
    x, y = position
    if x < 0 or x >= room_width or y < 0 or y >= room_height:
        # Out of bounds
        return

    if room[x][y] in ["plant", "tv", "bed"]:
        # Blocked by an object
        return

    if position in visited:
        # Already visited
        return

    visited.add(position)

    # Clean the tile if it is dirty
    if room[x][y] == 0:
        room[x][y] = 1

    # Update the robot's position and display the room
    robot_position = position
    draw_room(screen, room, robot_position, font)
    pygame.display.update()
    time.sleep(0.1)

    # Move in all possible directions (up, down, left, right)
    dfs(screen, font, (x, y - 1), room, visited)
    dfs(screen, font, (x, y + 1), room, visited)
    dfs(screen, font, (x - 1, y), room, visited)
    dfs(screen, font, (x + 1, y), room, visited)


