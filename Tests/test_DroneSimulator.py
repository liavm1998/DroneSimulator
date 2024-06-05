import os
import unittest

import numpy as np
from PIL import Image

from drone import Drone
from drone_sim import DroneSimulator
from map import Map


class TestDroneSimulator(unittest.TestCase):
    map1 = [
        ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
        ['W', 'P', 'P', 'P', 'P', 'P', 'P', 'W', 'W', 'W'],
        ['W', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'W', 'W'],
        ['W', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'W', 'W'],
        ['W', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'W', 'W'],
        ['W', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'W', 'W'],
        ['w', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'W', 'W'],
        ['W', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'W', 'W'],
        ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
        ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W']
    ]

    def test_find_start_position(self):
        # Create a DroneSimulator instance with a known map
        simulator = DroneSimulator('maps/p11.png', [0, 0])

        # Mock the map attribute with a known matrix
        simulator.map.map = self.map1

        # Call the method and assert the result

        result = simulator.find_start_position(simulator.map.map, 0)

        self.assertEqual(result, [4, 4])  # Expected start position
        self.assertEqual(simulator.isAttainable([4, 4]), True)

    def test_isAttainable(self):
        # Create a DroneSimulator instance with a known map
        simulator = DroneSimulator('maps/p11.png', [0, 0])

        # Mock the map attribute with a known matrix
        simulator.map.map = self.map1
        self.assertEqual(simulator.isAttainable([0, 0]), False)
        for i in range(len(simulator.map.map)):
            for j in range(len(simulator.map.map[0])):
                if i == 4 and j == 4 or i == 5 and j == 4 or i == 5 and j == 5:

                    self.assertEqual(simulator.isAttainable([i, j]), True)
                else:

                    self.assertEqual(simulator.isAttainable([i, j]), False)


class TestMap(unittest.TestCase):
    test_image_path = "testImage.png"
    path = 'Data'

    def create_test_image(self, file_path):

        # Define the size of the image
        width, height = 10, 10

        # Create a new RGB image
        img = Image.new('RGB', (width, height), color='white')

        # Define pixel colors
        wall_color = (0, 0, 0)  # Black
        passage_color = (255, 255, 255)  # White

        # Draw some walls and passages
        pixels = img.load()
        for i in range(width):
            for j in range(height):
                if (i == 0 or i == width - 1 or j == 0 or j == height - 1):  # Border walls
                    pixels[i, j] = wall_color
                else:
                    pixels[i, j] = passage_color

        # Save the image
        try:
            (img.save(file_path))
        except:
            os.makedirs(self.path, exist_ok=True)
            img.save(file_path)

    # Create test image

    def setUp(self):
        # Create a test image without yellow pixels
        self.test_image_path = "Data/testImage.png"
        self.create_test_image(self.test_image_path)
        self.map = Map(self.test_image_path)

    def test_map_loading(self):

        self.create_test_image(self.test_image_path)
        # Check if the map is loaded correctly
        expected_map = np.array([
            ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
            ['W', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'W'],
            ['W', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'W'],
            ['W', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'W'],
            ['W', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'W'],
            ['W', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'W'],
            ['W', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'W'],
            ['W', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'W'],
            ['W', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'W'],
            ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
        ], dtype='<U1')
        np.testing.assert_array_equal(self.map.map, expected_map)

    def test_no_yellow_pixels(self):
        # Ensure there are no yellow pixels in the map
        for row in self.map.map:
            for pixel in row:
                self.assertNotEqual(pixel, 'V')
                self.assertNotEqual(pixel, 'S')


class TestDrone(unittest.TestCase):
    def setUp(self):
        # Create a test image and Map object without yellow pixels
        self.test_image_path = "Data/testImage.png"
        TestMap.create_test_image(self, self.test_image_path)
        self.map = Map(self.test_image_path)

        # Initialize the Drone object
        self.drone = Drone(initial_position=[4, 4])

    def test_initialization(self):
        self.assertEqual(self.drone.position[0], 4)
        self.assertEqual(self.drone.position[1], 4)
        self.assertEqual(self.drone.radius, 10)
        self.assertEqual(self.drone.speed, 0)
        self.assertEqual(self.drone.max_speed, 3)
        self.assertEqual(self.drone.acceleration, 1)
        self.assertEqual(self.drone.orientation, 0)
        self.assertEqual(self.drone.battery, 100)
        self.assertAlmostEqual(self.drone.max_flight_time, 8 * 60)
        self.assertAlmostEqual(self.drone.kp, 2.5)
        self.assertAlmostEqual(self.drone.ki, 0.3)
        self.assertAlmostEqual(self.drone.kd, 0.15)

    def test_update_sensors(self):
        # Mock map_array for testing sensor updates
        map_array = self.map.map

        # Update sensors and check if the values are updated correctly
        sensors = self.drone.update_sensors(map_array)
        self.assertTrue(all(key in sensors for key in ['up', 'down', 'left', 'right']))
        self.assertIsInstance(sensors['up'], float)
        self.assertIsInstance(sensors['down'], float)
        self.assertIsInstance(sensors['left'], float)
        self.assertIsInstance(sensors['right'], float)
        self.drone.update_sensors(map_array)

        self.assertEqual(sensors['up'], 0.1)
        self.assertEqual(sensors['down'],  0.07500000000000001 )
        self.assertEqual(sensors['right'],  0.07500000000000001 )
        self.assertEqual(sensors['left'],  0.1)

    # def test_calculate_pid(self):
    #     target = 1.25
    #     current = 0.8
    #     control_signal = self.drone.calculate_pid(target, current)
    #     self.assertIsInstance(control_signal, float)
    #     self.assertNotEqual(control_signal, 0)
    # #
    def test_choose_left_or_right(self):

        direction = self.drone.choose_left_or_right()
        self.assertEqual(direction, 1)

        self.drone.distance_sensors['left'] = 0.5
        self.drone.distance_sensors['right'] = 1.0
        direction = self.drone.choose_left_or_right()
        self.assertEqual(direction, -1)

    def test_wall_ahead_maneuver(self):
        control_signal = 1.0
        initial_orientation = self.drone.orientation
        self.drone.distance_sensors['left'] = 0.1
        self.drone.distance_sensors['right'] = 0.07500000000000001
        result = initial_orientation + 4.0
        self.drone.wall_ahead_maneuver(control_signal)
        self.assertEqual(self.drone.orientation, result)

    def test_sudden_wall_maneuver(self):
        initial_orientation = self.drone.orientation
        self.drone.distance_sensors['left'] = 0.1
        self.drone.distance_sensors['right'] = 0.07500000000000001
        self.drone.sudden_wall_maneuver()
        self.assertEqual(self.drone.orientation, initial_orientation+180)

    def test_balancing_maneuver(self):
        control_signal = 3.0
        initial_orientation = self.drone.orientation
        self.drone.distance_sensors['left'] = 1.0
        self.drone.distance_sensors['right'] = 1.0
        self.drone.balancing_maneuver(control_signal)
        self.assertEqual(self.drone.orientation, 3)
        self.drone.distance_sensors['left'] = 0.1
        self.drone.distance_sensors['right'] = 0.07500000000000001
        self.drone.balancing_maneuver(control_signal)

        self.assertEqual(self.drone.orientation, 6)
    # def test_fly(self):
    #     # Mock initial conditions
    #     self.drone.battery = 100
    #     self.drone.start_time = time.time() - 1  # Ensure the drone can fly
    #
    #     # Simulate sensor data
    #     self.drone.distance_sensors = {'up': 1.0, 'down': 2.0, 'left': 0.5, 'right': 1.5}
    #
    #     initial_position = self.drone.position.copy()
    #     self.drone.fly()
    #
    #     # Check if the position has been updated
    #     self.assertNotEqual(self.drone.position[0], initial_position[0])
    #     self.assertNotEqual(self.drone.position[1], initial_position[1])


if __name__ == '__main__':
    unittest.main()
