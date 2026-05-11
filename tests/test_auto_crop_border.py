import os
import sys
import unittest

import numpy as np
from PIL import Image


ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NODES_DIR = os.path.join(ROOT_DIR, "nodes")
if NODES_DIR not in sys.path:
    sys.path.insert(0, NODES_DIR)

from image_auto_crop_border import AutoCropBorder, auto_crop_border_image, find_first_non_color_borders, pil2tensor

try:
    import torch  # noqa: F401
except ModuleNotFoundError:
    HAS_TORCH = False
else:
    HAS_TORCH = True


class AutoCropBorderTest(unittest.TestCase):
    def test_finds_white_border_offsets(self):
        image = Image.new("RGB", (10, 8), "white")
        for y in range(2, 6):
            for x in range(3, 8):
                image.putpixel((x, y), (10, 100, 200))

        borders = find_first_non_color_borders(image, (255, 255, 255), 50)

        self.assertEqual(borders, {
            "top": 2,
            "bottom": 2,
            "left": 3,
            "right": 2,
        })

    def test_crops_border_without_resize_back(self):
        image = Image.new("RGB", (10, 8), "white")
        for y in range(2, 6):
            for x in range(3, 8):
                image.putpixel((x, y), (10, 100, 200))

        result = auto_crop_border_image(image, "#FFFFFF", 50, resize_back=False, resize_method="BILINEAR")

        self.assertEqual(result.size, (5, 4))
        pixels = np.asarray(result)
        self.assertTrue(np.all(pixels == np.array([10, 100, 200], dtype=np.uint8)))

    def test_node_can_resize_result_back_to_original_size(self):
        if not HAS_TORCH:
            self.skipTest("torch is required for ComfyUI IMAGE tensor node execution")

        image = Image.new("RGB", (10, 8), "white")
        for y in range(2, 6):
            for x in range(3, 8):
                image.putpixel((x, y), (10, 100, 200))

        result_tensor, = AutoCropBorder.auto_crop_border(
            pil2tensor(image),
            "#FFFFFF",
            50,
            True,
            "NEAREST",
            "RGB",
        )

        self.assertEqual(tuple(result_tensor.shape), (1, 8, 10, 3))
        result_pixels = np.rint(result_tensor.numpy()[0] * 255).astype(np.uint8)
        self.assertTrue(np.all(result_pixels == np.array([10, 100, 200], dtype=np.uint8)))

    def test_returns_original_when_image_is_all_target_color(self):
        image = Image.new("RGB", (4, 3), "white")

        result = auto_crop_border_image(image, "#FFFFFF", 50, resize_back=False, resize_method="BILINEAR")

        self.assertEqual(result.size, (4, 3))
        self.assertEqual(result.getpixel((0, 0)), (255, 255, 255))


if __name__ == "__main__":
    unittest.main()
