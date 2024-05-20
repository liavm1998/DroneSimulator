from PIL import Image

class Map:
    def __init__(self, image_path, pixel_size=2.5):
        self.image_path = image_path
        self.pixel_size = pixel_size  # cm per pixel
        self.pixels_map = self._create_pixels_map()

    def _create_pixels_map(self):
        image = Image.open(self.image_path)
        grayscale_image = image.convert('L')
        pixels_map = []
        for y in range(grayscale_image.height):
            row = []
            for x in range(grayscale_image.width):
                row.append(grayscale_image.getpixel((x, y)))
            pixels_map.append(row)
        return pixels_map

    def get_pixels_map(self):
        return self.pixels_map

    def get_pixel_value(self, x, y):
        return self.pixels_map[y][x]

    def is_wall(self, x, y):
        return self.get_pixel_value(x, y) == 0
