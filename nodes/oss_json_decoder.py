import datetime
import json
import os

CATEGORY = "ComfyUI-Utils/Parsing"


class OSSJSONDecoder:
    """
    Decode an OSS-related JSON string and return individual outputs with defaults.
    Falls back to environment variables for credentials and auto-generates
    timestamp-based paths when image keypaths are missing.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "json_str": (
                    "STRING",
                    {
                        "multiline": True,
                        "default": "",
                        "placeholder": (
                            '{\n'
                            '  "oss_endpoint": "oss-cn-shenzhen.aliyuncs.com",\n'
                            '  "oss_bucket_name": "wownow-storage",\n'
                            '  "oss_access_key_id": "AKID...",\n'
                            '  "oss_access_key_secret": "AKSECRET...",\n'
                            '  "width": 1024,\n'
                            '  "height": 1024,\n'
                            '  "filename": "f3301718e9dbf7e7d703b73a144afa32.jpg"\n'
                            '}'
                        ),
                    },
                )
            }
        }

    RETURN_TYPES = (
        "STRING",
        "STRING",
        "STRING",
        "STRING",
        "INT",
        "INT",
        "STRING",
        "STRING",
        "STRING",
    )
    RETURN_NAMES = (
        "oss_endpoint",
        "oss_bucket_name",
        "oss_access_key_id",
        "oss_access_key_secret",
        "width",
        "height",
        "uv_image_keypath",
        "binary_image_keypath",
        "depth_image_keypath",
    )

    FUNCTION = "decode"
    CATEGORY = CATEGORY
    DESCRIPTION = (
        "Decode JSON string into OSS credentials and image keypaths, "
        "auto-generating missing paths with a timestamp."
    )

    def _as_str(self, value, default=""):
        if value is None:
            return default
        return str(value)

    def _as_int(self, value, default=0):
        if value is None or value == "":
            return default
        try:
            return int(value)
        except Exception:
            return default

    def _mask(self, secret, keep_start=3, keep_end=2):
        """Best-effort masking for logs so secrets are not exposed in full."""
        if not secret:
            return secret
        if len(secret) <= keep_start + keep_end:
            return "*" * len(secret)
        return (
            secret[:keep_start]
            + "*" * (len(secret) - keep_start - keep_end)
            + secret[-keep_end:]
        )

    def decode(self, json_str: str):
        data = {}
        if json_str and json_str.strip():
            try:
                data = json.loads(json_str)
                if not isinstance(data, dict):
                    data = {}
            except Exception:
                data = {}

        oss_endpoint = self._as_str(
            data.get("oss_endpoint", os.getenv("OSS_ENDPOINT", "oss-cn-shenzhen.aliyuncs.com"))
        )
        oss_bucket_name = self._as_str(
            data.get("oss_bucket_name", os.getenv("OSS_BUCKET_NAME", ""))
        )
        oss_access_key_id = self._as_str(
            data.get("oss_access_key_id", os.getenv("OSS_ACCESS_KEY_ID", ""))
        )
        oss_access_key_secret = self._as_str(
            data.get(
                "oss_access_key_secret", os.getenv("OSS_ACCESS_KEY_SECRET", "")
            )
        )

        width = self._as_int(data.get("width", 10), default=100)
        height = self._as_int(data.get("height", 10), default=100)

        filename_raw = self._as_str(data.get("filename", "")).strip()
        filename = os.path.splitext(filename_raw)[0] if filename_raw else "image"
        now_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

        def default_path(suffix):
            return f"infiniAI/generated/{now_str}/{filename}_{suffix}.png"

        uv_image_keypath = self._as_str(
            data.get("uv_image_keypath", default_path("uv"))
        )
        binary_image_keypath = self._as_str(
            data.get("binary_image_keypath", default_path("binary"))
        )
        depth_image_keypath = self._as_str(
            data.get("depth_image_keypath", default_path("depth"))
        )

        try:
            print(
                "[OSSJSONDecoder] Parsed:",
                {
                    "oss_endpoint": oss_endpoint,
                    "oss_bucket_name": oss_bucket_name,
                    "oss_access_key_id": self._mask(oss_access_key_id),
                    "oss_access_key_secret": self._mask(oss_access_key_secret),
                    "width": width,
                    "height": height,
                    "uv_image_keypath": uv_image_keypath,
                    "binary_image_keypath": binary_image_keypath,
                    "depth_image_keypath": depth_image_keypath,
                },
            )
        except Exception:
            pass

        return (
            oss_endpoint,
            oss_bucket_name,
            oss_access_key_id,
            oss_access_key_secret,
            width,
            height,
            uv_image_keypath,
            binary_image_keypath,
            depth_image_keypath,
        )


NODE_CLASS_MAPPINGS = {
    "Light-Tool: OSSJSONDecoder": OSSJSONDecoder,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Light-Tool: OSSJSONDecoder": "Light-Tool: Decode OSS JSON with Auto Path Generation",
}
