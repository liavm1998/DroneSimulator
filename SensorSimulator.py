import random
import numpy as np

class SensorSimulator:
    def __init__(self, drone, map_instance):
        self.drone = drone
        self.map = map_instance

    def get_distance_sensor_data(self, direction):
        # Simulate distance with a typical error of ±2%
        max_distance = 3.0  # in meters
        pixel_max_distance = max_distance / self.map.pixel_size  # convert to pixels
        error_factor = random.uniform(0.98, 1.02)
        
        distance = self._detect_wall_in_direction(direction, pixel_max_distance) * self.map.pixel_size
        distance_with_error = distance * error_factor
        return round(min(distance_with_error, max_distance), 2)

    def _detect_wall_in_direction(self, direction, pixel_max_distance):
        # Detect wall in the given direction and return the distance to the wall in pixels
        dx, dy = 0, 0
        if direction == 'left':
            dx = -1
        elif direction == 'right':
            dx = 1
        elif direction == 'forward':
            dy = -1
        elif direction == 'backward':
            dy = 1

        for pixel_distance in range(int(pixel_max_distance)):
            x = int(self.drone.x + dx * pixel_distance)
            y = int(self.drone.y + dy * pixel_distance)
            if x < 0 or x >= len(self.map.pixel_map[0]) or y < 0 or y >= len(self.map.pixel_map):
                return pixel_distance  # Edge of the map
            if self.map.pixel_map[y][x] == 'wall':
                print('was in wall but painted')
                self.map.pixel_map[y][x] = 'painted'  # Paint the passage yellow
                return pixel_distance  # Wall detected
            elif self.map.pixel_map[y][x] == 'passage':
                print('painted')
                self.map.pixel_map[y][x] = 'painted'  # Paint the passage yellow

        return pixel_max_distance  # No wall detected within max distance

    def get_speed_sensor_data(self):
        # Simulate speed sensor (optical flow)
        return round(self.drone.speed * random.uniform(0.98, 1.02), 2)

    def get_imu_data(self):
        # Simulate IMU data for orientation
        return round(self.drone.orientation * random.uniform(0.98, 1.02), 2)

    def get_barometer_data(self):
        # Simulate barometer data for altitude
        return round(self.drone.altitude * random.uniform(0.98, 1.02), 2)

    def get_sensor_data(self):
        distance_sensors = {
            'left': self.get_distance_sensor_data('left'),
            'right': self.get_distance_sensor_data('right'),
            'forward': self.get_distance_sensor_data('forward'),
            'backward': self.get_distance_sensor_data('backward')
        }
        speed = self.get_speed_sensor_data()
        orientation = self.get_imu_data()
        altitude = self.get_barometer_data()

        return {
            'distance_sensors': distance_sensors,
            'speed': speed,
            'orientation': orientation,
            'altitude': altitude
        }

