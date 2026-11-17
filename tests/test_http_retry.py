import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import call, patch

import httpx

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "nodes"))
from light_tool_http import get_with_retry, put_bytes_with_retry, put_file_with_retry


class HttpRetryTest(unittest.TestCase):
    def setUp(self):
        self.url = "https://storage.example.test/image?signature=test"
        self.sleep = self.enter_patch("light_tool_http.time.sleep")

    def enter_patch(self, name):
        patcher = patch(name)
        self.addCleanup(patcher.stop)
        return patcher.start()

    def test_download_recovers_after_timeout_and_503(self):
        get = self.enter_patch("light_tool_http.httpx.get")
        get.side_effect = [httpx.ReadTimeout("timeout"), httpx.Response(503),
                           httpx.Response(200, content=b"image")]
        response = get_with_retry(self.url, follow_redirects=True)
        self.assertEqual(response.content, b"image")
        self.assertEqual(get.call_args_list, [call(self.url, follow_redirects=True)] * 3)
        self.assertEqual(self.sleep.call_args_list, [call(1), call(2)])

    def test_download_propagates_third_network_failure(self):
        get = self.enter_patch("light_tool_http.httpx.get")
        get.side_effect = httpx.ConnectError("offline")
        with self.assertRaises(httpx.ConnectError):
            get_with_retry(self.url)
        self.assertEqual(get.call_count, 3)
        self.assertEqual(self.sleep.call_count, 2)

    def test_image_put_returns_third_retryable_response(self):
        put = self.enter_patch("light_tool_http.httpx.put")
        put.return_value = httpx.Response(429)
        response = put_bytes_with_retry(self.url, b"png", timeout=120)
        self.assertEqual(response.status_code, 429)
        self.assertEqual(put.call_args_list, [call(self.url, content=b"png", timeout=120)] * 3)
        self.assertEqual(self.sleep.call_args_list, [call(1), call(2)])

    def test_expired_signature_is_not_retried(self):
        put = self.enter_patch("light_tool_http.httpx.put")
        put.return_value = httpx.Response(403)
        self.assertEqual(put_bytes_with_retry(self.url, b"png").status_code, 403)
        put.assert_called_once()
        self.sleep.assert_not_called()

    def test_file_put_replays_entire_body_after_disconnect(self):
        bodies = []
        headers = {"Content-Type": "image/png"}

        def receive(url, *, content, **kwargs):
            self.assertEqual(url, self.url)
            self.assertEqual(kwargs, {"headers": headers, "timeout": 120})
            bodies.append(content.read())
            if len(bodies) == 1:
                raise httpx.RemoteProtocolError("disconnected")
            return httpx.Response(200)

        put = self.enter_patch("light_tool_http.httpx.put")
        put.side_effect = receive
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "image.png"
            path.write_bytes(b"whole image")
            response = put_file_with_retry(self.url, path, headers=headers, timeout=120)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(bodies, [b"whole image", b"whole image"])
