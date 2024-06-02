import pygame
import numpy as np
from PIL import Image
import os
import random
import time

class Map:
    def __init__(self, file_path=None):
        self.map = None
        self.file_path = file_path
        if file_path:
            self.map = self.load_map(file_path)

    def load_map(self, filename):
        # Open the image file
        img = Image.open(filename)
        img = img.convert('RGB')  # Ensure the image is in RGB mode
        self.image = img
        # Get image dimensions
        width, height = img.size
        print(f'map2 height:{height},map2 width:{width}')    
        # Initialize map representation with an empty array
        map_data = np.full((height, width), ' ', dtype='<U1')

        for y in range(height):
            for x in range(width):
                # Get pixel value
                r, g, b = img.getpixel((x, y))

                # Determine type of pixel
                if (r, g, b) == (0, 0, 0):
                    map_data[y, x] = 'W'  # Wall
                elif (r, g, b) == (255, 255, 255):
                    map_data[y, x] = 'P'  # Passage
                elif (r, g, b) == (255, 255, 0):
                    map_data[y, x] = 'L'  # Location visited

        return map_data

    def save_png(self, file_path):
        """
        Save the current map to a PNG file.
        """
        if self.map:
            # Create directories if they do not exist
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            self.map.save(file_path)
        else:
            print("No map to save")

    def get_pixel_type(self, x, y):
        """
        Get the type of the pixel at (x, y).
        Returns 'wall', 'passage', or 'visited'.
        """
        if not self.map:
            return None
        r, g, b = self.map.getpixel((x, y))
        if (r, g, b) == (0, 0, 0):
            return 'wall'
        elif (r, g, b) == (255, 255, 255):
            return 'passage'
        elif (r, g, b) == (255, 255, 0):
            return 'visited'
        else:
            return 'unknown'

    def set_pixel(self, x, y, pixel_type):
        """
        Set the type of the pixel at (x, y).
        pixel_type should be 'wall', 'passage', or 'visited'.
        """
        if not self.map:
            return
        if pixel_type == 'wall':
            color = (0, 0, 0)
        elif pixel_type == 'passage':
            color = (255, 255, 255)
        elif pixel_type == 'visited':
            color = (255, 255, 0)
        else:
            return
        self.map.putpixel((x, y), color)
