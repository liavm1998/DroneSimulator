from PIL import Image,ImageDraw
import random
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)


class Map:
    def __init__(self,image_path, pixel_size=2.5):
        self.image_path = image_path
        self.pixel_map = self._create_pixel_map()
        self.pixel_size=pixel_size

    def _create_pixel_map(self):
        image = Image.open(self.image_path).convert('RGB')
        width, height = image.size
        pixel_map = []

        for y in range(height):
            row = []
            for x in range(width):
                r, g, b = image.getpixel((x, y))
                if (r, g, b) == WHITE:
                    row.append('passage')
                elif (r, g, b) == BLACK:
                    row.append('wall')
                else:
                    row.append('unknown')
            pixel_map.append(row)

        return pixel_map

    def display_pixel_map(self):
        for row in self.pixel_map:
            print(' '.join(row))
        

    def save_pixel_map_to_file(self, output_path,pixel_size=2):
        # Determine the dimensions of the new image based on the pixel_map size
        width = len(self.pixel_map[0]) * pixel_size
        height = len(self.pixel_map) * pixel_size
        
        # Create a new image with the calculated dimensions
        new_image = Image.new("RGB", (width, height))
        draw = ImageDraw.Draw(new_image)

        print("memory issue bro")
        # Paint the map based on the pixel_map
        for y, row in enumerate(self.pixel_map):
            for x, pixel_type in enumerate(row):
                if pixel_type == 'wall':
                    draw.rectangle([(x * pixel_size, y * pixel_size), ((x + 1) * pixel_size, (y + 1) * pixel_size)],
                                   fill=BLACK)
                elif pixel_type == 'passage':
                    draw.rectangle([(x * pixel_size, y * pixel_size), ((x + 1) * pixel_size, (y + 1) * pixel_size)],
                                   fill=WHITE)
                elif pixel_type == 'painted':
                    draw.rectangle([( x * pixel_size, y * pixel_size), ((x + 1) * pixel_size, (y + 1) * pixel_size)],
                                   fill=YELLOW)

        # Save the new image as PNG or JPEG based on the output_path extension
        if output_path.lower().endswith('.png'):
            new_image.save(output_path, "PNG")
        elif output_path.lower().endswith('.jpg') or output_path.lower().endswith('.jpeg'):
            new_image.save(output_path, "JPEG")
        else:
            raise ValueError("Unsupported file format. Please provide a path with '.png', '.jpg', or '.jpeg' extension.")


    def get_random_white_pixel(self):
        white_pixels = [(x, y) for y, row in enumerate(self.pixel_map) for x, pixel in enumerate(row) if pixel == 'passage']
        return random.choice(white_pixels)