import time
import numpy as np
import SensorSimulator


class Drone:
    def __init__(self, map_obj, start_x, start_y):
        self.map = map_obj
        self.x = start_x
        self.y = start_y

        self.vx = 0
        self.vy = 0
    
        self.orientation = 0  # degrees, 0 is north/up
        self.sensor_simulator = SensorSimulator(map_obj)
        self.battery_life = 480  # seconds
        self.time_step = 0.1  # seconds

    def get_battery_status(self):
        return self.battery_life

    def get_sensor_readings(self):
        return self.sensor_simulator.get_sensor_readings(self.x, self.y)

    def get_imu_readings(self):
        return {
            'orientation': self.orientation,
            'acceleration': (self.vx / self.time_step, self.vy / self.time_step)
        }

    def move(self, pitch, roll):
        if self.battery_life <= 0: # 240 and write return
            print("Battery depleted")
            return

        ax = min(max(pitch, -1), 1) * 1  # max acceleration 1 m/s^2
        ay = min(max(roll, -1), 1) * 1   # max acceleration 1 m/s^2
    

        self.vx = min(max(self.vx + ax * self.time_step, -3), 3)  # max speed 3 m/s
        self.vy = min(max(self.vy + ay * self.time_step, -3), 3)  # max speed 3 m/s
        

        self.x += self.vx * self.time_step * 100  # convert to cm
        self.y += self.vy * self.time_step * 100  # convert to cm
        

        self.battery_life -= self.time_step
        time.sleep(self.time_step)

    def get_position(self):
        return self.x, self.y


