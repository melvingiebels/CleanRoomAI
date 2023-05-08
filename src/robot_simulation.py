import time
from room_generation import draw_room, room_width, room_height
import pygame
from collections import deque


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


from collections import deque

def bfs(screen, font, position, room):

    visited = set()
    queue = deque([(position, room)])
    draw_room(screen, room, position, font)

    while queue:
        position, room = queue.popleft()
        x, y = position

        if x < 0 or x >= room_width or y < 0 or y >= room_height:
            # Out of bounds
            continue

        if room[x][y] in ["plant", "tv", "bed"]:
            # Blocked by an object
            continue

        if position in visited:
            # Already visited
            continue

        visited.add(position)

        # Clean the tile if it is dirty
        if room[x][y] == 0:
            room[x][y] = 1

        # Update the robot's position and display the room
        robot_position = position
        draw_room(screen, room, robot_position, font)
        pygame.display.update()
        time.sleep(0.1)

        if position == (0, 0):
            # Reached the starting point, return
            return

        # Add neighboring positions to the queue
        neighbors = [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)]
        for neighbor in neighbors:
            queue.append((neighbor, room))

# Example usage:

# Example usage:
