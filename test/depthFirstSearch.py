import pygame
import random
import sys
import time

# Step 1: Create a visual representation of the 2D living room
pygame.init()
window_size = (800, 600)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("My Living Room")

room_width = 8
room_height = 10
tile_size = 50

# Generate a living room
room = [[0 for y in range(room_height)] for x in range(room_width)]

# Define the objects to add to the room
objects = [
    {"name": "plant", "width": 1, "height": 1},
    {"name": "tv", "width": 3, "height": 1},
    {"name": "bed", "width": 2, "height": 5},
]

# Check for overlapping objects and add one object of each type to the room
for obj in objects:
    obj_coords = []
    for x in range(obj["width"]):
        for y in range(obj["height"]):
            obj_coords.append((x, y))

    # Check if any of the object coordinates are already occupied
    is_occupied = True
    while is_occupied:
        obj_x = random.randint(0, room_width - obj["width"])
        obj_y = random.randint(0, room_height - obj["height"])
        is_occupied = False
        for coord in obj_coords:
            x = obj_x + coord[0]
            y = obj_y + coord[1]
            if room[x][y] != 0:
                is_occupied = True
                break
            # Check if the tile is too close to another object
            for x_offset in range(-1, obj["width"] + 1):
                for y_offset in range(-1, obj["height"] + 1):
                    if 0 <= x + x_offset < room_width and 0 <= y + y_offset < room_height:
                        if room[x + x_offset][y + y_offset] != 0:
                            is_occupied = True
                            break
                if is_occupied:
                    break
            if is_occupied:
                break

    # Add the object to the room
    for x in range(obj_x, obj_x + obj["width"]):
        for y in range(obj_y, obj_y + obj["height"]):
            room[x][y] = obj["name"]

# Set up the robot's initial position
robot_position = (0, 0)

# Step 2: Implement statistics tracking
font = pygame.font.Font(None, 36)

#implement a timer that shows the time when the robot is cleaning
timer = pygame.time.Clock()
fps = 60

def dfs(position, room, visited):
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
    global robot_position
    robot_position = position
    draw_room(room, robot_position)
    pygame.display.update()
    time.sleep(0.1)

    # Move in all possible directions (up, down, left, right)
    dfs((x, y - 1), room, visited)
    dfs((x, y + 1), room, visited)
    dfs((x - 1, y), room, visited)
    dfs((x + 1, y), room, visited)

def draw_room(room, robot_position):
    for x in range(room_width):
        for y in range(room_height):
            if room[x][y] == 0:
                # Dirty tile
                tile_color = (255, 255, 255)
            elif room[x][y] == 1:
                # Clean tile
                tile_color = (0, 255, 0)
            elif room[x][y] == "plant":
                # Plant tile
                tile_color = (0, 0, 255)
            elif room[x][y] == "tv":
                # Tv tile
                tile_color = (255, 255, 0)
            elif room[x][y] == "bed":
                # Bed tile
                tile_color = (128, 0, 128)
            tile_rect = pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
            pygame.draw.rect(screen, tile_color, tile_rect)

            # Draw the robot as a red rectangle
            robot_rect = pygame.Rect(
                robot_position[0] * tile_size,
                robot_position[1] * tile_size,
                tile_size,
                tile_size,
            )
            pygame.draw.rect(screen, (255, 0, 0), robot_rect)

            # Calculate the total number of spaces occupied by objects
            occupied_spaces = sum(obj["width"] * obj["height"] for obj in objects)

            # Display the current statistics of the room
            text = font.render(
                "Cleaned: {} / Total: {}".format(
                    sum(row.count(1) for row in room),
                    room_width * room_height - occupied_spaces
                ),
                True,
                (0, 0, 0),
            )
            screen.blit(text, (10, 10))
            time = font.render(
                "Time: {}".format(pygame.time.get_ticks() // 1000),
                True,
                (0, 0, 0),
            )
            screen.blit(time, (10, 30))


while True:
    timer.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Perform depth-first search
                dfs(robot_position, room, set())
                pygame.display.update()