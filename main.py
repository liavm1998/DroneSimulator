
from drone_sim import DroneSimulator

# Example usage
if __name__ == "__main__":
    map_image_path = 'maps/p11.png'
    initial_drone_position = [100, 100]  # Initial position of the drone
    simulator = DroneSimulator(map_image_path, initial_drone_position)
    simulator.run()
