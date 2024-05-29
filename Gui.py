import pygame
import numpy as np
import threading
from Map import Map
from Drone import Drone
from ControllerLogic import ControllerLogic
import sys


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 225, 0)
RED = (255, 0, 0)  # Color for the drone

def draw_map(screen, map_obj, drone, scale):
    for y, row in enumerate(map_obj.pixel_map):
        for x, pixel_type in enumerate(row):
            color = BLACK if pixel_type == 'wall' else WHITE if pixel_type == 'passage' else YELLOW
            rect = pygame.Rect(x * scale, y * scale, scale, scale)
            pygame.draw.rect(screen, color, rect)
    
    # Draw the drone as a navigation arrow
    drone_x = int(drone.x * scale)
    drone_y = int(drone.y * scale)
    drone_size = int(scale * 10)  # Size of the drone
    arrow_length = int(scale * 1.5)  # Length of the arrow

    # Calculate the vertices of the arrow
    orientation_rad = np.radians(drone.orientation)
    base = (drone_x + arrow_length * np.cos(orientation_rad), drone_y + arrow_length * np.sin(orientation_rad))
    tip = (drone_x + drone_size * np.cos(orientation_rad), drone_y + drone_size * np.sin(orientation_rad))
    left_tail = (drone_x + drone_size * np.cos(orientation_rad + 5 * np.pi / 6), drone_y + drone_size * np.sin(orientation_rad + 5 * np.pi / 6))
    right_tail = (drone_x + drone_size * np.cos(orientation_rad - 5 * np.pi / 6), drone_y + drone_size * np.sin(orientation_rad - 5 * np.pi / 6))

    # Draw the arrow
    pygame.draw.polygon(screen, RED, [base, left_tail, tip, right_tail])

def main():
    pygame.init()

    image_path = sys.argv[1]
    map_obj = Map(image_path)

    # Create the Drone object with a random starting position
    i, j = map_obj.get_random_white_pixel()
    drone = Drone(map_obj, i, j)

    #apply logic to the drone
    logic = ControllerLogic(drone)
    
    # Calculate the map dimensions
    map_width = len(map_obj.pixel_map[0]) * map_obj.pixel_size
    map_height = len(map_obj.pixel_map) * map_obj.pixel_size

    # Get screen dimensions
    display_info = pygame.display.Info()
    screen_width = display_info.current_w
    screen_height = display_info.current_h

    # Scale the window if it's larger than the screen
    scale = map_obj.pixel_size
    if map_width > screen_width or map_height > screen_height:
        scale = min(screen_width / len(map_obj.pixel_map[0]), screen_height / len(map_obj.pixel_map))

    width = int(len(map_obj.pixel_map[0]) * scale)
    height = int(len(map_obj.pixel_map) * scale)
    screen = pygame.display.set_mode((width, height))

    pygame.display.set_caption('Drone Simulator')

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Move the drone (for testing purposes, you can update pitch and roll as needed)
        # drone.move(pitch=0.1, roll=0, duration=1)  # Update these values for your test

        # print("x: ", drone.x)
        # print("y: ", drone.y)
        print(drone.sensor_simulator.get_sensor_data())
        logic.explore_and_return()
        screen.fill(WHITE)
        draw_map(screen, map_obj, drone, scale)
        pygame.display.flip()

        clock.tick(60)  # Limit to 60 FPS

    pygame.quit()

if __name__ == "__main__":
    main()