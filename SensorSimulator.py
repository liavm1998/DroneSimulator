import random
import numpy as np

class SensorSimulator:
    def __init__(self, drone, map_instance):
        self.drone = drone
        self.map = map_instance

    def get_distance_sensor_data(self, direction):
        # Simulate distance with a typical error of ±2%
        max_distance = 300  # in m
        pixel_max_distance = max_distance / self.map.pixel_size  # convert to pixels
        error_factor = random.uniform(0.98, 1.02)
        
        distance = self._detect_wall_in_direction(direction, pixel_max_distance) * self.map.pixel_size
        distance_with_error = distance * error_factor
        return round(min(distance_with_error, max_distance), 2)

    def _detect_wall_in_direction(self, direction, pixel_max_distance):
        # Detect wall in the given direction and return the distance to the wall in pixels
        dx, dy = direction
        x , y = self.drone.x , self.drone.y
        for pixel_distance in range(int(pixel_max_distance)):
            x = int(x + dx * pixel_distance)
            y = int(y + dy * pixel_distance)
            if x < 0 or x >= len(self.map.pixel_map[0]) or y < 0 or y >= len(self.map.pixel_map):
                return pixel_distance  # Edge of the map
            
            elif self.map.pixel_map[y][x] == 'wall':
                return pixel_distance  # Wall detected
            
            elif self.map.pixel_map[y][x] == 'passage':
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
            'left': self.get_distance_sensor_data((-1,0)),
            'right': self.get_distance_sensor_data((1,0)),
            'forward': self.get_distance_sensor_data((0,1)),
            'backward': self.get_distance_sensor_data((0,-1))
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

