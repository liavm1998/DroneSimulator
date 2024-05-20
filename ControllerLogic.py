import heapq

class ControllerLogic:
    def __init__(self, drone):
        self.drone = drone

    def explore_and_return(self):
        start_x, start_y = self.drone.x, self.drone.y
        while self.drone.get_battery_status() > 0:
            sensor_data = self.drone.get_sensor_data()

            # Check if there are unexplored areas nearby
            if 'passage' in sensor_data['distance_sensors'].values():
                # Move towards unexplored area if not surrounded by yellow or black pixels
                if not self._surrounded_by_yellow_or_black():
                    self._move_towards_unexplored()
                else:
                    self._rotate_to_find_unexplored()
            else:
                # No unexplored areas nearby, return to start point
                self._return_to_start(start_x, start_y)
                break

    def _surrounded_by_yellow_or_black(self):
        sensor_data = self.drone.get_sensor_data()
        return all(value in ['painted', 'wall'] for value in sensor_data['distance_sensors'].values())

    def _move_towards_unexplored(self):
        # Move forward by default if there is a passage in front
        self.drone.move(pitch=1)

    def _rotate_to_find_unexplored(self):
        # Rotate clockwise to find unexplored areas
        for _ in range(4):
            self.drone.move(roll=-90)  # Rotate 90 degrees clockwise
            sensor_data = self.drone.get_sensor_data()
            if 'passage' in sensor_data['distance_sensors'].values():
                # If passage is found after rotation, break the loop
                break

    def _return_to_start(self, start_x, start_y):
        # Use A* algorithm to find the shortest path back to start
        path = self._find_shortest_path(start_x, start_y)
        if path:
            # Follow the path back to the starting point
            for x, y in path:
                dx = x - self.drone.x
                dy = y - self.drone.y
                # Calculate angle to return to next point in the path
                target_angle = np.degrees(np.arctan2(dy, dx))
                # Adjust orientation towards next point
                angle_diff = target_angle - self.drone.orientation
                self.drone.move(roll=angle_diff, duration=1)
                # Move towards next point in the path
                self.drone.move(pitch=1)

    def _find_shortest_path(self, start_x, start_y):
        # Use A* algorithm to find the shortest path back to start
        open_list = [(0, (self.drone.x, self.drone.y))]
        heapq.heapify(open_list)
        parent = {(self.drone.x, self.drone.y): None}
        visited = set()

        while open_list:
            cost, (x, y) = heapq.heappop(open_list)
            if (x, y) == (start_x, start_y):
                path = []
                while (x, y) in parent:
                    path.append((x, y))
                    x, y = parent[(x, y)]
                path.reverse()
                return path
            if (x, y) not in visited:
                visited.add((x, y))
                for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    new_x, new_y = x + dx, y + dy
                    if 0 <= new_x < len(self.drone.map.pixel_map[0]) and 0 <= new_y < len(self.drone.map.pixel_map) \
                            and self.drone.map.pixel_map[new_y][new_x] != 'wall' and (new_x, new_y) not in visited:
                        heapq.heappush(open_list, (cost + 1, (new_x, new_y)))
                        parent[(new_x, new_y)] = (x, y)
        return None
