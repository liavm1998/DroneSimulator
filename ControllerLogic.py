import heapq
import numpy as np

class ControllerLogic:
    def __init__(self, drone):
        self.drone = drone
        self.explored = set()
        self.frontiers = []
        self.target = None

    def explore_and_return(self):
        i = 0
        start_x, start_y = self.drone.x, self.drone.y
        while self.drone.get_battery_status() > 0:
            self.explored.add((self.drone.x, self.drone.y))
            self._scan_area()
            # Update frontiers based on sensor data
            self._update_frontiers()
            # Determine next target if none exists or target has been reached
            if not self.target or (self.drone.x, self.drone.y) == self.target:
                self.target = self._find_next_target()
            if self.target:
                self._move_towards_target()
            else:
                # If no unexplored areas found, return to start point
                self._return_to_start(start_x, start_y)
                break
        
        

    def _scan_area(self):
        # Scan by rotating left and right
        for angle in [-90, 0, 90]:
            self.drone.move(roll=angle, duration=1)
            sensor_data = self.drone.get_sensor_data()
            self._update_frontiers(sensor_data)

    def _update_frontiers(self, sensor_data=None):
        if sensor_data is None:
            sensor_data = self.drone.get_sensor_data()
        directions = ['forward', 'left', 'right', 'backward']
        for direction in directions:
            if sensor_data['distance_sensors'][direction] == 'passage':
                target_coords = self._get_target_coords(direction)
                if target_coords and target_coords not in self.explored and target_coords not in self.frontiers:
                    self.frontiers.append(target_coords)

    def _get_target_coords(self, direction):
        if direction == 'front':
            new_x = self.drone.x + np.cos(np.radians(self.drone.orientation))
            new_y = self.drone.y + np.sin(np.radians(self.drone.orientation))
        elif direction == 'left':
            new_x = self.drone.x + np.cos(np.radians(self.drone.orientation - 90))
            new_y = self.drone.y + np.sin(np.radians(self.drone.orientation - 90))
        elif direction == 'right':
            new_x = self.drone.x + np.cos(np.radians(self.drone.orientation + 90))
            new_y = self.drone.y + np.sin(np.radians(self.drone.orientation + 90))
        elif direction == 'back':
            new_x = self.drone.x + np.cos(np.radians(self.drone.orientation + 180))
            new_y = self.drone.y + np.sin(np.radians(self.drone.orientation + 180))
        else:
            return None
        return (new_x, new_y)

    def _find_next_target(self):
        # Prioritize nearby unexplored areas
        sensor_data = self.drone.get_sensor_data()
        for direction, status in sensor_data['distance_sensors'].items():
            if status == 'passage':
                target_coords = self._get_target_coords(direction)
                if target_coords and target_coords not in self.explored:
                    return target_coords

        # If no immediate unexplored areas, select a frontier
        if self.frontiers:
            return self.frontiers.pop(0)
        return None

    def _move_towards_target(self):
        target_x, target_y = self.target
        dx = target_x - self.drone.x
        dy = target_y - self.drone.y
        target_angle = np.degrees(np.arctan2(dy, dx))
        angle_diff = target_angle - self.drone.orientation
        self.drone.move(roll=angle_diff, duration=1)
        self.drone.move(pitch=1, duration=1)

    def _return_to_start(self, start_x, start_y):
        path = self._find_shortest_path(start_x, start_y)
        if path:
            for x, y in path:
                dx = x - self.drone.x
                dy = y - self.drone.y
                target_angle = np.degrees(np.arctan2(dy, dx))
                angle_diff = target_angle - self.drone.orientation
                self.drone.move(roll=angle_diff, duration=1)
                self.drone.move(pitch=1, duration=1)

    def _find_shortest_path(self, start_x, start_y):
        open_list = [(0, (self.drone.x, self.drone.y))]
        heapq.heapify(open_list)
        parent = {(self.drone.x, self.drone.y): (None,None)}
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
                            and self.drone.map.pixel_map[int(new_y)][int(new_x)] != 'wall' \
                            and (new_x, new_y) not in visited:
                        heapq.heappush(open_list, (cost + 1, (new_x, new_y)))
                        parent[(new_x, new_y)] = (x, y)
        return None
