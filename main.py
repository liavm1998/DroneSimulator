import sys
from drone_sim import DroneSimulator


# Example usage
if __name__ == "__main__":
    map_image_path = 'maps/p14.png'
    if len(sys.argv) > 1:
        map_image_path = sys.argv[1]
    else:
        print("No map image path passed")

    

    initial_drone_position = [100, 100]  # Initial position of the drone
    simulator = DroneSimulator(map_image_path, initial_drone_position)
    simulator.run()



