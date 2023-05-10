import random
import pygame

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

DIRTY_TILE_IMAGE = pygame.image.load("images/dirty_tile.jpg")
CLEAN_TILE_IMAGE = pygame.image.load("images/clean_tile.jpg")
PLANT_IMAGE = pygame.image.load("images/plant_clean.jpg")
TV_IMAGE = pygame.image.load("images/tv_dirty.jpg")
TV_IMAGE = pygame.transform.scale(TV_IMAGE, (tile_size * 3, tile_size))
BED_IMAGE = pygame.image.load("images/bed.jpg")

ROBOT_IMAGE = pygame.image.load("images/robot.png")
ROBOT_IMAGE = pygame.transform.scale(ROBOT_IMAGE, (tile_size, tile_size))


def draw_room(screen, room, robot_position, font, steps):
    for x in range(room_width):
        for y in range(room_height):
            if room[x][y] == 0:
                # Dirty tile
                screen.blit(DIRTY_TILE_IMAGE, (x * tile_size, y * tile_size))
            elif room[x][y] == 1:
                # Clean tile
                screen.blit(CLEAN_TILE_IMAGE, (x * tile_size, y * tile_size))
            elif room[x][y] == "plant":
                # Plant tile
                screen.blit(PLANT_IMAGE, (x * tile_size, y * tile_size))
            elif room[x][y] == "tv":
                # Tv tile
                tile_color = (255, 255, 0)
                tile_rect = pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
                pygame.draw.rect(screen, tile_color, tile_rect)
                # screen.blit(TV_IMAGE, (x * tile_size, y * tile_size))
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
    screen.blit(ROBOT_IMAGE, robot_rect)

    # Calculate the total number of spaces occupied by objects
    occupied_spaces = sum(obj["width"] * obj["height"] for obj in objects)

    # Display the current statistics of the room
    text = font.render(
        "Cleaned: {} / Total: {} | Steps: {}".format(
            sum(row.count(1) for row in room),
            room_width * room_height - occupied_spaces,
            steps
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