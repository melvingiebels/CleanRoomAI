import random
import pygame
from zmq import NULL

room_width = 8
room_height = 10
tile_size = 50

objects = [
    {"name": "plant", "width": 1, "height": 1},
    {"name": "tv", "width": 3, "height": 1},
    {"name": "bed", "width": 2, "height": 5},
]

def generate_room(starting_point):
    
    
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

    robot_position = starting_point

    return room, robot_position

def draw_room(screen, room, robot_position, font):
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
