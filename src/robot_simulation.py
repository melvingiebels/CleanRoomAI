import time
from room_generation import draw_room, room_width, room_height
import pygame
from collections import deque


def dfs(screen, font, position, room, visited, steps):
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
    draw_room(screen, room, robot_position, font, steps)
    pygame.display.update()
    time.sleep(0.1)

    # Move in all possible directions (up, down, left, right)
    dfs(screen, font, (x, y - 1), room, visited, steps=steps+1)
    dfs(screen, font, (x, y + 1), room, visited, steps=steps+1)
    dfs(screen, font, (x - 1, y), room, visited, steps=steps+1)
    dfs(screen, font, (x + 1, y), room, visited, steps=steps+1)


from collections import deque
from collections import deque

def bfs(screen, font, position, room):
    starting_point = position
    visited = set()
    queue = deque([(position, room)])
    draw_room(screen, room, position, font, steps=0)
    path = []
    parent = {}  # Store parent position for each visited position

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
        draw_room(screen, room, robot_position, font, steps=0)
        pygame.display.update()
        time.sleep(0.1)

        if position == (0, 0):
            # Reached the starting point, break the loop
            break

        # Add neighboring positions to the queue and store their parent positions
        neighbors = [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)]
        for neighbor in neighbors:
            if neighbor not in parent:  # Only add neighbors not already in the parent dictionary
                queue.append((neighbor, room))
                parent[neighbor] = position

    # Reconstruct the shortest path from the destination to the starting point
    position = (0, 0)
    while position != starting_point:
        path.append(position)
        position = parent[position]
    path.append(starting_point)
    path.reverse()

    # Walk the path to the destination
    walk_back(screen, font, room, path)


def walk_back(screen, font, room, path):
    for position in path:
        print(position)
        robot_position = position
        draw_room(screen, room, robot_position, font, steps=len(path)-1)
        pygame.display.update()
        time.sleep(0.5)



import heapq
from math import sqrt

def a_star(screen, font, position, room):
    starting_point = position
    visited = set()
    queue = [(0, position, room)]
    path = []
    parent = {}  # Store parent position for each visited position
    cost = {position: 0}

    while queue:
        queue.sort()
        _, position, room = queue.pop(0)
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
        draw_room(screen, room, robot_position, font, steps=0)
        pygame.display.update()
        time.sleep(0.1)

        if position == (0, 0):
            # Reached the starting point, break the loop
            break

        # Add neighboring positions to the queue and store their parent positions
        neighbors = [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)]
        for neighbor in neighbors:
            if neighbor not in parent:  # Only add neighbors not already in the parent dictionary
                cost[neighbor] = cost[position] + 1
                queue.append((cost[neighbor] + heuristic(neighbor), neighbor, room))
                parent[neighbor] = position

    # Reconstruct the shortest path from the destination to the starting point
    position = (0, 0)
    while position != starting_point:
        path.append(position)
        position = parent[position]
    path.append(starting_point)
    path.reverse()

    # Walk the path to the destination
    walk_back(screen, font, room, path)

def heuristic(position):
    # Calculate the Euclidean distance from position to the charging station
    x, y = position
    return ((x - 0) ** 2 + (y - 0) ** 2) ** 0.5