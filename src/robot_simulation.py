import time
from room_generation import draw_room, room_width, room_height
import pygame
from collections import deque
import heapq
from math import sqrt
from collections import deque
import random



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
    dfs(screen, font, (x, y - 1), room, visited, steps=steps + 1)
    dfs(screen, font, (x, y + 1), room, visited, steps=steps + 1)
    dfs(screen, font, (x - 1, y), room, visited, steps=steps + 1)
    dfs(screen, font, (x + 1, y), room, visited, steps=steps + 1)


def bfs(screen, font, position, room):
    starting_point = position
    visited = set()
    queue = deque([(position, room)])
    draw_room(screen, room, position, font, steps=0)
    path = [] # Stores the shortest path from the destination to the starting point
    parent = {}  # Store parent position for each visited position

    while queue:
        pygame.event.get()  # Add this line to prevent the window from freezing
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

        # Pathing tile back to charging station
        room[x][y] = 2

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
            if (
                neighbor not in parent
            ):  # Only add neighbors not already in the parent dictionary
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


def a_star(screen, font, position, room):
    starting_point = position
    visited = set()
    queue = [(0, position, room)]
    path = []
    parent = {}  # Store parent position for each visited position
    cost = {position: 0}

    while queue:
        pygame.event.get()  # Add this line to prevent the window from freezing
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

        # Pathing tile back to charging station
        room[x][y] = 2

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
            if (
                neighbor not in parent
            ):  # Only add neighbors not already in the parent dictionary
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


def random_cleaning(screen, font, position, room, is_displayed):
    moves = 0

    while True:
        x, y = position

        # Check if the robot is trapped
        trapped = True
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            if (
                (x + dx) >= 0
                and (x + dx) < room_width
                and (y + dy) >= 0
                and (y + dy) < room_height
                and room[x + dx][y + dy] not in ["plant", "tv", "bed"]
            ):
                trapped = False
                break

        if trapped:
            print("Faulty room. Regenerating...")
            return None

        # Randomly choose a direction to move
        dx, dy = random.choice([(0, -1), (0, 1), (-1, 0), (1, 0)])

        # Check if the move is valid
        if (
            (x + dx) < 0
            or (x + dx) >= room_width
            or (y + dy) < 0
            or (y + dy) >= room_height
        ):
            # Out of bounds
            continue

        if room[x + dx][y + dy] in ["plant", "tv", "bed"]:
            # Blocked by an object
            continue

        # Update the position
        position = (x + dx, y + dy)

        # Clean the tile if it is dirty
        if room[x + dx][y + dy] == 0:
            room[x + dx][y + dy] = 1

        moves += 1

        if is_displayed:
            draw_room(screen, room, position, font, steps=moves)
            pygame.display.update()

        # Check if all tiles are cleaned
        if count_dirty_tiles(room) == 0:
            break

        # Check if it's taking too many steps
        if moves >= 50000:
            print("Faulty room. Regenerating...")
            return None

    # draw_room(screen, room, position, font, steps=moves)
    # pygame.display.update()
    print(f"Random cleaning took {moves} steps.")
    return position, moves


def count_dirty_tiles(room):
    count = 0
    for row in room:
        for tile in row:
            if tile == 0:
                count += 1
    return count


def walk_back(screen, font, room, path):
    for position in path:
        pygame.event.get()  # Add this line to prevent the window from freezing
        print(position)
        robot_position = position
        draw_room(screen, room, robot_position, font, steps=len(path) - 1)
        pygame.display.update()
        time.sleep(0.2)


def heuristic(position):
    # Calculate the Euclidean distance from position to the charging station
    x, y = position
    return ((x - 0) ** 2 + (y - 0) ** 2) ** 0.5 



def sweep_room(screen, font, position, room):
    # Initialize the boundaries
    top = 0
    bottom = room_height - 1
    left = 0
    right = room_width - 1

    # Initialize the direction
    direction = 0  # 0: right, 1: down, 2: left, 3: up

    moves = 0

    while top <= bottom and left <= right:
        pygame.event.get()  # Add this line to prevent the window from freezing

        if direction == 0:  # Move right
            for x in range(left, right + 1):
                position = (x, top)
                if room[x][top] != "plant":  # Check if the tile contains a plant
                    clean_tile(screen, font, room, position, moves)
                    moves += 1
                else:
                    # Move around the plant until a valid position is found
                    while room[x][top] == "plant":
                        position = (x - 1, top + 1)
                        clean_tile(screen, font, room, position, moves)
                        moves += 1
                        x -= 1
                    position = (x, top + 1)
                    break
            top += 1
        elif direction == 1:  # Move down
            for y in range(top, bottom + 1):
                position = (right, y)
                if room[right][y] != "plant":
                    clean_tile(screen, font, room, position, moves)
                    moves += 1
                else:
                    # Move around the plant until a valid position is found
                    while room[right][y] == "plant":
                        position = (right - 1, y - 1)
                        clean_tile(screen, font, room, position, moves)
                        moves += 1
                        y -= 1
                    position = (right - 1, y)
                    break
            right -= 1
        elif direction == 2:  # Move left
            for x in range(right, left - 1, -1):
                position = (x, bottom)
                if room[x][bottom] != "plant":
                    clean_tile(screen, font, room, position, moves)
                    moves += 1
                else:
                    # Move around the plant until a valid position is found
                    while room[x][bottom] == "plant":
                        position = (x + 1, bottom - 1)
                        clean_tile(screen, font, room, position, moves)
                        moves += 1
                        x += 1
                    position = (x, bottom - 1)
                    break
            bottom -= 1
        elif direction == 3:  # Move up
            for y in range(bottom, top - 1, -1):
                position = (left, y)
                if room[left][y] != "plant":
                    clean_tile(screen, font, room, position, moves)
                    moves += 1
                else:
                    # Move around the plant until a valid position is found
                    while room[left][y] == "plant":
                        position = (left + 1, y + 1)
                        clean_tile(screen, font, room, position, moves)
                        moves += 1
                        y += 1
                        position = (left + 1, y)
                        break
            left += 1
        direction = (direction + 1) % 4  # Update the direction

    print(f"Spiral inward cleaning took {moves} steps.")


def clean_tile(screen, font, room, position, moves):
    x, y = position

    if room[x][y] != "plant":
        # Clean the tile if it is not a plant
        if room[x][y] == 0:
            room[x][y] = 1

        # Update the robot's position and display the room
        robot_position = position
        draw_room(screen, room, robot_position, font, steps=moves)
        pygame.display.update()
        time.sleep(0.1)
    # Update the robot's position and display the room
    robot_position = position
    draw_room(screen, room, robot_position, font, steps=moves)
    pygame.display.update()
    time.sleep(0.1)


directions = [[1, 0], [0, -1], [0, 1], [-1, 0]]

def dfscleaning_ai(screen, font, position, room):
    start_x, start_y = position
    x, y = position

    dirty_tiles = count_dirty_tiles(room)
    tiles = 0
    totalTilesPassed = 0

    continue_loop = True

    while continue_loop:
        pygame.event.get()

        # First go below if possible
        dir = 0

        new_row = y + directions[dir][1]
        new_col = x + directions[dir][0]

        print(new_row, new_col)

        while not is_valid_move(room, new_row, new_col):
            dir += 1
            print(dir)
            if dir > 3:
                continue_loop = False
                new_row = y + 0
                new_col = x + 0
                break;
            else:
                new_row = y + directions[dir][1]
                new_col = x + directions[dir][0]

        if not (new_row == start_y and new_col == start_x):
            room[new_row][new_col] = 1
            tiles += 1
            totalTilesPassed += 1

        position = (new_row, new_col)
        print(position)
        y, x = position

        draw_room(screen, room, position, font, steps=0)
        pygame.display.update()
        time.sleep(0.1)

        if tiles == dirty_tiles:
            print ("All tiles cleaned")
            print (tiles, dirty_tiles)
            continue_loop = False
    return totalTilesPassed


def is_valid_move(room, new_row, new_col):

    if new_row < 0 or new_row >= len(room) or new_col < 0 or new_col >= len(room[0]):
        print("Out of bounds")
        return False

    if (room[new_row][new_col] == 1 or room[new_row][new_col] == 3):
        return False

    if room[new_row][new_col] in ["plant", "tv", "bed"]:
        print("Blocked by an object")
        return False

    return True






def bfs_cleaning(screen, font, position, room):
    dirty_tiles = set()  # Stores the positions of dirty tiles

    # Initialize the queue, visited set, parent dictionary, and dirty tiles list
    queue = deque([position])
    visited = set()
    parent = {}
    dirty_tiles.add(position)

    while queue:
        current_position = queue.popleft()

        if current_position in visited:
            continue

        visited.add(current_position)

        x, y = current_position

        if len(dirty_tiles) == 0:
            # All tiles are cleaned, exit the loop
            break

        # Check the neighboring positions
        neighbors = [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)]
        for neighbor in neighbors:
            if neighbor not in visited and is_valid_position(room, neighbor):
                # Enqueue the neighboring position and update the parent dictionary
                queue.append(neighbor)
                parent[neighbor] = current_position
                if room[neighbor[0]][neighbor[1]] == 0:
                    # Add dirty tiles to the list
                    dirty_tiles.add(neighbor)

    # Clean the remaining dirty tiles
    while dirty_tiles:
        closest_tile = find_closest_tile(position, dirty_tiles)
        path = reconstruct_path(closest_tile, parent)
        walk_path(screen, font, room, path)
        position = closest_tile
        x, y = position
        room[x][y] = 1
        dirty_tiles.remove(position)
        draw_room(screen, room, closest_tile, font, steps=len(path))
        pygame.display.update()

    pygame.display.update()


def is_valid_position(room, position):
    x, y = position
    return 0 <= x < room_width and 0 <= y < room_height and room[x][y] != "plant" and room[x][y] != "tv" and room[x][y] != "bed"


def find_closest_tile(position, dirty_tiles):
    x, y = position
    closest_tile = None
    closest_distance = float("inf")

    for tile in dirty_tiles:
        tile_x, tile_y = tile
        distance = abs(x - tile_x) + abs(y - tile_y)
        if distance < closest_distance:
            closest_distance = distance
            closest_tile = tile

    return closest_tile


def reconstruct_path(tile, parent):
    path = []
    while tile in parent:
        path.append(tile)
        tile = parent[tile]
    path.reverse()
    return path

def walk_path(screen, font, room, path):
    for position in path:
        pygame.event.get()
        x, y = position
        room[x][y] = 1  # Pathing tile
        draw_room(screen, room, position, font, steps=len(path))
        pygame.display.update()
        time.sleep(0.05)
