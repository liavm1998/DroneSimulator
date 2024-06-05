import pygame
import numpy as np
from map import Map
from drone import Drone


class DroneSimulator:
    def __init__(self, map_file_path, initial_drone_position):
        self.map = Map(map_file_path)
        initial_drone_position = self.find_start_position(self.map.map)
        self.drone = Drone(initial_drone_position)

    def find_start_position(self, matrix, boarder=50):

        for i in range(boarder + 3, len(matrix) - boarder - 1):
            for j in range(boarder + 3, len(matrix[0]) - boarder - 1):
                if matrix[i][j] == 'P' and self.isAttainable([i, j]):
                    return [j, i]

    def isAttainable(self, pixel):
        attainable = True
        if pixel[0] < 3 or pixel[1] < 3 or pixel[0] > len(self.map.map) - 3 or pixel[1] > len(self.map.map[0]) - 3:
            return False

        for i in range(pixel[0] - 3, min(pixel[0] + 3, (len(self.map.map) - 1))):
            for j in range(pixel[1] - 3, min(pixel[1] + 3, (len(self.map.map[0]) - 1))):
                if self.map.map[i][j] == 'W':
                    # print( pixel ,"not attainable because ", i, j)
                    return False
        # print(pixel, "is attainable")
        return True

    def run(self):
        # Initialize Pygame
        pygame.init()
        screen_width, screen_height = self.map.map.shape[::-1]
        screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption('Drone Simulator')

        # Main loop
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Update drone sensors based on the current map
            visited_dir = self.drone.update_sensors(self.map.map)
            self.map.set_pixel(round(self.drone.position[0]), round(self.drone.position[1]), 'V')
            # TODO need logic to draw visited_dirs in yellow here
            self.drone.fly()

            # Draw map
            screen.fill((255, 255, 255))  # White background
            for y in range(len(self.map.map)):
                for x in range(len(self.map.map[0])):
                    color = (0, 0, 0) if self.map.map[y][x] == 'W' else (
                        (255, 255, 255) if self.map.map[y][x] == 'P' else (255, 255, 0) if self.map.map[y][
                                                                                               x] == 'S' else (
                            0, 0, 255))

                    pygame.draw.rect(screen, color, (x, y, 1, 1))

            # Draw drone (for now, just a red circle at its position)
            drone_pos = (int(self.drone.position[0]), int(self.drone.position[1]))
            pygame.draw.circle(screen, (255, 0, 0), drone_pos, 5)  # Red circle

            pygame.display.flip()

        # pygame.quit()
