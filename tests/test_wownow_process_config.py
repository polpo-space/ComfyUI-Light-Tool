import json
import os
import sys
import unittest


ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NODES_DIR = os.path.join(ROOT_DIR, "nodes")
if NODES_DIR not in sys.path:
    sys.path.insert(0, NODES_DIR)

from data_tool import DeserializeWownowProcessConfig


class DeserializeWownowProcessConfigTest(unittest.TestCase):
    def test_decode_outputs_process_switches(self):
        config = {
            "width": 1024,
            "height": 768,
            "origin_image_url": "https://cdn.example.com/source.png",
            "uv_image_put_url": "https://storage.example.com/uv.png",
            "binary_image_put_url": "https://storage.example.com/binary.png",
            "depth_image_put_url": "https://storage.example.com/depth.png",
            "depth_border_image_url": "https://cdn.example.com/depth-border.png",
            "normalmap_image_put_url": "https://storage.example.com/normal.png",
            "outpaint_image_put_url": "https://storage.example.com/outpaint.png",
            "crop_image_put_url": "https://storage.example.com/crop.png",
        }

        result = DeserializeWownowProcessConfig().decode(json.dumps(config))

        self.assertEqual(
            result,
            (
                1024,
                768,
                "https://cdn.example.com/source.png",
                "https://storage.example.com/uv.png",
                "https://storage.example.com/binary.png",
                "https://storage.example.com/depth.png",
                "https://storage.example.com/normal.png",
                "https://storage.example.com/outpaint.png",
                "https://storage.example.com/crop.png",
                True,
                True,
                True,
                "https://cdn.example.com/depth-border.png",
            ),
        )

    def test_decode_infers_process_switches_from_put_urls(self):
        config = {
            "uv_image_put_url": "https://storage.example.com/uv.png",
            "depth_image_put_url": "https://storage.example.com/depth.png",
            "crop_image_put_url": "https://storage.example.com/crop.png",
            "need_crop_white_border": False,
            "need_uv": False,
            "need_depth": False,
        }

        result = DeserializeWownowProcessConfig().decode(json.dumps(config))

        self.assertEqual(result[9:], (True, True, True, ""))

    def test_decode_defaults_missing_process_switches_to_false(self):
        result = DeserializeWownowProcessConfig().decode("{}")

        self.assertEqual(result[8:], ("", False, False, False, ""))


if __name__ == "__main__":
    unittest.main()
