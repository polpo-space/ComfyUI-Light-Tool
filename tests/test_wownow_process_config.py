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
            "normalmap_image_put_url": "https://storage.example.com/normal.png",
            "outpaint_image_put_url": "https://storage.example.com/outpaint.png",
            "need_crop_white_border": True,
            "need_uv": True,
            "need_depth": False,
        }

        result = DeserializeWownowProcessConfig().decode(json.dumps(config))

        self.assertEqual(result[8:], (True, True, False))

    def test_decode_defaults_missing_process_switches_to_false(self):
        result = DeserializeWownowProcessConfig().decode("{}")

        self.assertEqual(result[8:], (False, False, False))


if __name__ == "__main__":
    unittest.main()
