import os
import sys
import unittest


ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NODES_DIR = os.path.join(ROOT_DIR, "nodes")
if NODES_DIR not in sys.path:
    sys.path.insert(0, NODES_DIR)

try:
    from light_tool import SaveImageToSignedPutURL, SaveToSignedPutURL
except ModuleNotFoundError as exc:
    LIGHT_TOOL_IMPORT_ERROR = exc
else:
    LIGHT_TOOL_IMPORT_ERROR = None


class SignedPutUploadTest(unittest.TestCase):
    def setUp(self):
        if LIGHT_TOOL_IMPORT_ERROR is not None:
            self.skipTest(f"light_tool dependencies are unavailable: {LIGHT_TOOL_IMPORT_ERROR}")

    def test_image_upload_skips_empty_put_url_without_images(self):
        node = SaveImageToSignedPutURL()

        self.assertEqual(
            node.check_lazy_status(None, "", "", "PNG", 120),
            [],
        )
        self.assertEqual(node.save_image(None, "", "", "PNG", 120), ("",))

    def test_image_upload_requests_images_when_put_url_is_present(self):
        node = SaveImageToSignedPutURL()

        self.assertEqual(
            node.check_lazy_status(None, "https://storage.example.com/upload.png", "", "PNG", 120),
            ["images"],
        )

    def test_file_upload_skips_empty_put_url_without_file(self):
        node = SaveToSignedPutURL()

        self.assertEqual(
            node.check_lazy_status(None, "", "", "application/octet-stream", "", 120),
            [],
        )
        self.assertEqual(
            node.save(None, "", "", "application/octet-stream", "", 120),
            ("",),
        )


if __name__ == "__main__":
    unittest.main()
