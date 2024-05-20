import time
import numpy as np

class SensorSimulator:
    def __init__(self, map_obj, drone_radius=10, max_distance=300):
        self.map_obj = map_obj
        self.drone_radius = drone_radius
        self.max_distance = max_distance

    def get_distance(self, x, y, direction):
        distance = self.max_distance
        step_size = self.map_obj.pixel_size
        x, y = x / step_size, y / step_size
        delta_x, delta_y = 0, 0

        if direction == 'forward':
            delta_y = -1
        elif direction == 'backward':
            delta_y = 1
        elif direction == 'left':
            delta_x = -1
        elif direction == 'right':
            delta_x = 1

        for d in range(1, int(self.max_distance / step_size)):
            check_x = int(x + d * delta_x)
            check_y = int(y + d * delta_y)
            if self.map_obj.is_wall(check_x, check_y):
                distance = d * step_size
                break

        return min(self.max_distance, distance)

    def get_sensor_readings(self, x, y):
        return {
            'forward': self.get_distance(x, y, 'forward'),
            'backward': self.get_distance(x, y, 'backward'),
            'left': self.get_distance(x, y, 'left'),
            'right': self.get_distance(x, y, 'right')
        }
