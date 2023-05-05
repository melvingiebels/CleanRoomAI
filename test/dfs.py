import pygame
import time

def dfs(position, room, visited, room_width, room_height, screen, objects, font):
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
    draw_room(room, robot_position, room_width, room_height, screen, objects, font)
    pygame.display.update()
    time.sleep(0.1)

    # Move in all possible directions (up, down, left, right)
    dfs((x, y - 1), room, visited, room_width, room_height, screen, objects, font)
    dfs((x, y + 1), room, visited, room_width, room_height, screen, objects, font)
    dfs((x - 1, y), room, visited, room_width, room_height, screen, objects, font)
    dfs((x + 1, y), room, visited, room_width, room_height, screen, objects, font)



def draw_room(room, robot_position, room_width, room_height, screen, objects, font, tile_size=50):
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
