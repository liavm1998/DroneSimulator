import unittest

from drone_sim import DroneSimulator


class TestDroneSimulator(unittest.TestCase):
    def test_find_start_position(self):
        # Create a DroneSimulator instance with a known map
        simulator = DroneSimulator('maps/p11.png', [0, 0])


        # Mock the map attribute with a known matrix
        simulator.map.map = [
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'W', 'W'],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'W', 'W', 'W'],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'W', 'W'],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'W', 'W'],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'W', 'W'],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'W', 'W'],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'W', 'W'],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'W', 'W'],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'W', 'W'],
            ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W']
        ]

        # Call the method and assert the result

        result = simulator.find_start_position(simulator.map.map,0)

        self.assertEqual(result, [4, 4])  # Expected start position


if __name__ == '__main__':
    unittest.main()
