
import numpy as np
from PIL import Image
import time
from map import Map



def calculate_direction(orientation_degrees):
    # Convert orientation from degrees to radians
    orientation_degrees = orientation_degrees % 360
    radians = np.radians(orientation_degrees)
    
    # Calculate direction components
    delta_x = np.cos(radians)
    delta_y = np.sin(radians)
    
    return delta_x, delta_y


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
        self.kp = 2.5  # Proportional gain
        self.ki = 0.3  # Integral gain
        self.kd = 0.15  # Derivative gain
        self.integral = 0
        self.previous_error = 0

    def update_sensors(self, map_array):
        drone_x, drone_y = int(self.position[0]), int(self.position[1])
        sensor_range = 120  # How far the sensors can sense in pixels (1m)

        def measure_distance_in_direction(vec):
            dx, dy = vec
            distance = 0
            for i in range(1, sensor_range + 1):
                nx, ny = drone_x + i * dx, drone_y + i * dy
                if 0 <= nx < map_array.shape[1] and 0 <= ny < map_array.shape[0]:
                    if map_array[round(ny), round(nx)] == 'W':
                        break
                    if map_array[round(ny), round(nx)] == 'P':
                        map_array[round(ny), round(nx)] = 'S'
                    distance += 1
                else:
                    break
            return distance * 0.025  # Convert to meters (2.5 cm per pixel)

        
        self.distance_sensors['up'] = measure_distance_in_direction(calculate_direction(orientation_degrees=self.orientation))
        self.distance_sensors['down'] = measure_distance_in_direction(calculate_direction(orientation_degrees=self.orientation+180))
        self.distance_sensors['left'] = measure_distance_in_direction(calculate_direction(orientation_degrees=self.orientation+90))
        self.distance_sensors['right'] = measure_distance_in_direction(calculate_direction(orientation_degrees=self.orientation+270))
        return self.distance_sensors

    def calculate_pid(self, target, current):
        error = target - current
        self.integral += error
        derivative = error - self.previous_error
        self.previous_error = error
        return self.kp * error + self.ki * self.integral + self.kd * derivative
    

    def choose_left_or_right(self):
        if self.distance_sensors['left'] < self.distance_sensors['right']:
            return -1
        return 1
    
    def wall_ahead_maneuver(self,control_signal ):
        dir = self.choose_left_or_right()
        self.orientation +=  dir * 4 * control_signal
        self.orientation =  self.orientation % 360
    
    def sudden_wall_maneuver(self ):
        # stop choose new direction and start again
        dir = self.choose_left_or_right()
        if dir == 1 and self.distance_sensors['left'] > 0.4:
            self.orientation += 90
        elif dir == -1 and self.distance_sensors['right'] > 0.4:
            self.orientation -= 90
        else:
            # deadend go back
            self.orientation += 180
        

    def balancing_maneuver(self,control_signal):
        dir = self.choose_left_or_right()
        self.orientation +=  dir * control_signal
        self.orientation =  self.orientation % 360
    
    def fly(self):
        if self.battery > 0:
            # Calculate the control signal
            if self.distance_sensors['up'] == 3:
                print('integral should be 0')
                self.integral = 0
            desired_distance = 1.25  # Desired distance to the wall in meters
            danger_distance = 0.4
            sensor_values = list(self.distance_sensors.values())
            closest_distance = min(sensor_values)
            control_signal = self.calculate_pid(desired_distance, closest_distance)
            
            # Adjust speed and orientation based on control signal
            self.speed = max(0, min(self.max_speed, self.speed + self.acceleration * 0.5 * control_signal))
            if self.distance_sensors['up'] < danger_distance:
                self.sudden_wall_maneuver()
            elif self.distance_sensors['up'] < desired_distance:
                self.wall_ahead_maneuver(control_signal)
            # need balance manevour
            
            elif self.distance_sensors['right'] != self.distance_sensors['left']:
                self.balancing_maneuver(control_signal=control_signal)
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
            print("integral:", self.integral)
            # time.sleep(0.1)  # Simulate 10 times a second
            print(f'orientations is {self.orientation}')