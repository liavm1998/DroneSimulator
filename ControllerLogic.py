import numpy as np

class ControllerLogic:
    def __init__(self, drone):
        self.drone = drone

    def explore_map(self):
        while self.drone.get_battery_status() > 0:
            # Example of simple exploration strategy: random walk
            pitch = np.random.uniform(-1, 1)  # randomly change speed
            roll = np.random.uniform(-1, 1)   # randomly change direction
            duration = 1

            self.drone.move(pitch, roll, duration)

            # Simulate scanning by getting sensor data
            sensor_data = self.drone.get_sensor_data()
            print(f"Sensor data at ({self.drone.x}, {self.drone.y}): {sensor_data}")

            # Optionally, save the map state at intervals or based on certain criteria
            # self.drone.save_map("current_map_state.png")