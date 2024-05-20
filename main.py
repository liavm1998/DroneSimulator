

import Map
import Drone

input_map = Map.Map('maps/p11.png')

my_drone = Drone.Drone(input_map, 40 ,40)
my_drone.get_sensor_data()

my_drone.save_map('outputs/p_out.png')
