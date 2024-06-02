
import numpy as np
from PIL import Image
import time
from map import Map


class Drone:
    def __init__(self, initial_position):
        self.position = initial_position
        self.radius = 10  # in cm
        self.distance_sensors = {'up': 0, 'down': 0, 'left': 0, 'right': 0}  # in meters
        self.speed = 0  # in m/s
        self.orientation = 0  # in degrees
        self.battery = 100  # in percentage
        self.max_flight_time = 8 * 60  # in seconds
        self.last_update_time = time.time()
        self.max_speed = 3  # in m/s
        self.acceleration = 1  # in m/s^2


    def update_sensors(self, map_array):
        # Get drone position in array coordinates
        drone_x, drone_y = int(self.position[0]), int(self.position[1])
        # Update distance sensors
        
        for direction in self.distance_sensors:
            distance = 0
            if direction == 'up':
                for i in range(drone_y - 1, -1, -1):  # Scan upwards
                    if map_array[i, drone_x] != 'W':
                        break    
                    distance += 1
                    
            elif direction == 'down':
                for i in range(drone_y + 1, len(map_array)):  # Scan downwards
                    if map_array[i, drone_x] == 'W':
                        break
                    distance += 1
            elif direction == 'left':
                for i in range(drone_x - 1, -1, -1):  # Scan leftwards
                    if map_array[drone_y, i] == 'W':
                        break
                    distance += 1
            elif direction == 'right':
                for i in range(drone_x + 1, len(map_array[0])):  # Scan rightwards
                    if map_array[drone_y, i] == 'W':
                        break
                    distance += 1

            self.distance_sensors[direction] = distance
        return self.distance_sensors
    def fly(self):
            if self.battery > 0:
                # Calculate new position based on speed and orientation
                delta_time = time.time() - self.last_update_time
                self.speed = min(self.speed + self.acceleration * delta_time, self.max_speed)
                distance_moved = self.speed * delta_time
                # TODO calculate direction with PID control
                delta_x = distance_moved * np.cos(np.radians(self.orientation))
                delta_y = distance_moved * np.sin(np.radians(self.orientation))
                self.position[0] += delta_x
                self.position[1] += delta_y
                self.last_update_time = time.time()

                print("Flying... Current Position:", self.position)
                print("Distance Sensors:", self.distance_sensors)
                time.sleep(0.1)  # Simulate 10 times a second
