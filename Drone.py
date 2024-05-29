import numpy as np
import SensorSimulator

class Drone:
    map = -1
    x = -1
    y = -1
    def __init__(self, input_map, start_x=- 1, start_y=-1):
        self.map = input_map
        self.x = start_x
        self.y = start_y
        if start_x<0 or start_y <0 :
            self.x, self.y = self.map.get_random_white_pixel()
        self.battery = 480  # max flight time in seconds
        self.speed = 0  # current speed in m/s
        self.orientation = 0  # angle in degrees
        self.altitude = 0  # height in meters
        self.sensor_simulator = SensorSimulator.SensorSimulator(self, input_map)


    def move(self, pitch=0, roll=0, duration=1):
        # Update orientation based on pitch and roll
        self.orientation += roll * duration
        self.orientation = self.orientation % 360  # keep orientation within 0-359 degrees

        # Update speed based on pitch
        self.speed += pitch * duration
        self.speed = min(max(self.speed, 0), 3)  # limit speed between 0 and 3 m/s

        # Update position based on speed and orientation
        rad_orientation = np.radians(self.orientation)
        dx = self.speed * np.cos(rad_orientation) * duration
        dy = self.speed * np.sin(rad_orientation) * duration

        self.x += dx / self.map.pixel_size  # converting to pixel units
        self.y += dy / self.map.pixel_size  # converting to pixel units

        # Decrease battery
        self.battery -= duration
        if self.battery <= 0:
            print("Battery depleted. Drone landing.")
            self.speed = 0

    def get_battery_status(self):
        return self.battery

    def get_sensor_data(self):
        return self.sensor_simulator.get_sensor_data()
    
    def save_map(self, out_path):
        self.map.save_pixel_map_to_file(out_path)
