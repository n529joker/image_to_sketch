import cv2 as cv
import numpy as np
import base64

class ImageProcessor:
    def __init__(self, image_path, brightness_factor=0.9, edge_color=(0, 0, 255)):
        self.image = cv.imread(image_path)
        self.brightness = brightness_factor
        self.edge_color = edge_color

    def adjust_brightness(self, image):
        hsv_image = cv.cvtColor(image, cv.COLOR_RGB2HSV)
        h, s, v = cv.split(hsv_image)
        v = cv.multiply(v, self.brightness)
        v = np.clip(v, 0, 255).astype(hsv_image.dtype)
        adjusted_hsv_image = cv.merge([h, s, v])
        adjusted_image = cv.cvtColor(adjusted_hsv_image, cv.COLOR_HSV2BGR)
        return adjusted_image

    def get_sketch(self):
        gray = cv.cvtColor(self.image, cv.COLOR_BGR2GRAY)

        # Invert grayscale image
        inverted = cv.bitwise_not(gray)

        # Apply Gaussian blur to inverted image
        blurred = cv.GaussianBlur(inverted, (21, 21), 0, 0)

        # Sketch effect
        sketch = cv.divide(gray, 255 - blurred, scale=256)

        # Edge detection
        edges = cv.Canny(sketch, 100, 200)

        # Apply specified color to edges
        colored_edges = np.zeros_like(self.image)
        colored_edges[:] = self.edge_color
        colored_edges = cv.bitwise_and(colored_edges, colored_edges, mask=edges)

        # Combine sketch and colored edges
        final_sketch = cv.addWeighted(
            cv.cvtColor(sketch, cv.COLOR_GRAY2BGR), 1.0, colored_edges, 1.0, 0
        )

        brightened_image = self.adjust_brightness(final_sketch)        
        _, buffer = cv.imencode('.png', brightened_image)
        return {'image': base64.b64encode(buffer).decode('utf-8')}
