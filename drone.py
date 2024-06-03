
import numpy as np
from PIL import Image
import time
from map import Map

class Drone:
    def __init__(self, initial_position):
        self.position = np.array(initial_position, dtype=float)
        self.radius = 10  # in cm
        self.distance_sensors = {'up': 0, 'down': 0, 'left': 0, 'right': 0}  # in meters
        self.speed = 0  # in m/s
        self.max_speed = 3  # in m/s
        self.acceleration = 1  # in m/s^2
        self.orientation = 0  # in degrees
        self.battery = 100  # in percentage
        self.max_flight_time = 8 * 60  # in seconds
        self.last_update_time = time.time()

        # PID controller parameters
        self.kp = 2.0  # Proportional gain
        self.ki = 0.1  # Integral gain
        self.kd = 0.05  # Derivative gain
        self.integral = 0
        self.previous_error = 0

    def update_sensors(self, map_array):
        drone_x, drone_y = int(self.position[0]), int(self.position[1])
        sensor_range = 40  # How far the sensors can sense in pixels (1m)

        def measure_distance_in_direction(dx, dy):
            distance = 0
            for i in range(1, sensor_range + 1):
                nx, ny = drone_x + i * dx, drone_y + i * dy
                if 0 <= nx < map_array.shape[1] and 0 <= ny < map_array.shape[0]:
                    if map_array[ny, nx] == 'W':
                        break
                    distance += 1
                else:
                    break
            return distance * 0.025  # Convert to meters (2.5 cm per pixel)

        self.distance_sensors['up'] = measure_distance_in_direction(0, -1)
        self.distance_sensors['down'] = measure_distance_in_direction(0, 1)
        self.distance_sensors['left'] = measure_distance_in_direction(-1, 0)
        self.distance_sensors['right'] = measure_distance_in_direction(1, 0)

    def calculate_pid(self, target, current):
        error = target - current
        self.integral += error
        derivative = error - self.previous_error
        self.previous_error = error
        return self.kp * error + self.ki * self.integral + self.kd * derivative

    def fly(self):
        if self.battery > 0:
            # Calculate the control signal
            desired_distance = 2  # Desired distance to the wall in meters
            sensor_values = list(self.distance_sensors.values())
            closest_distance = min(sensor_values)
            control_signal = self.calculate_pid(desired_distance, closest_distance)
            
            # Adjust speed and orientation based on control signal
            self.speed = max(0, min(self.max_speed, self.speed + self.acceleration * control_signal))
            # best_direction_is
            if self.distance_sensors['left'] < desired_distance:
                print(f'left dir')
                self.orientation += 2 * control_signal
            elif self.distance_sensors['right'] < desired_distance:
                print(f'right dir')
                self.orientation -= 2* control_signal

            # Calculate new position based on speed and orientation
            delta_time = time.time() - self.last_update_time
            distance_moved = self.speed * delta_time
            delta_x = distance_moved * np.cos(np.radians(self.orientation))
            delta_y = distance_moved * np.sin(np.radians(self.orientation))
            self.position[0] += delta_x
            self.position[1] += delta_y

            self.last_update_time = time.time()

            print("Flying... Current Position:", self.position)
            print("Speed:", self.speed)
            print("Distance Sensors:", self.distance_sensors)
            time.sleep(0.1)  # Simulate 10 times a second