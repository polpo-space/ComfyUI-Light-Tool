"""
@author: Hmily
@title: ComfyUI-Light-Tool
@nickname: ComfyUI-Light-Tool
@description: Auto crop image borders for ComfyUI.
"""
import os
import sys

import numpy as np
from PIL import Image
from PIL.Image import Resampling

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


RESIZE_METHODS = {
    "LANCZOS": Resampling.LANCZOS,
    "BICUBIC": Resampling.BICUBIC,
    "NEAREST": Resampling.NEAREST,
    "BILINEAR": Resampling.BILINEAR,
}


def tensor2pil(t_image):
    return Image.fromarray(np.clip(255.0 * t_image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))


def pil2tensor(image):
    import torch

    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)


def _parse_hex_color(hex_color):
    value = hex_color.strip().lstrip("#")
    if len(value) != 6:
        raise ValueError("Light-Tool: target_color must be a 6-digit hex color, for example #FFFFFF.")
    try:
        return tuple(int(value[index:index + 2], 16) for index in (0, 2, 4))
    except ValueError as exc:
        raise ValueError("Light-Tool: target_color must be a valid hex color, for example #FFFFFF.") from exc


def _image_rgb_over_background(image, background=(255, 255, 255)):
    rgba = image.convert("RGBA")
    data = np.asarray(rgba).astype(np.float32)
    alpha = data[:, :, 3:4] / 255.0
    rgb = data[:, :, :3] * alpha + np.array(background, dtype=np.float32) * (1.0 - alpha)
    return np.rint(rgb).astype(np.int16)


def find_first_non_color_borders(image, target_color=(255, 255, 255), tolerance=50):
    rgb = _image_rgb_over_background(image)
    target = np.array(target_color, dtype=np.int16)
    non_target = np.any(np.abs(rgb - target) > int(tolerance), axis=2)

    rows = np.where(np.any(non_target, axis=1))[0]
    cols = np.where(np.any(non_target, axis=0))[0]
    if rows.size == 0 or cols.size == 0:
        return None

    return {
        "top": int(rows[0]),
        "bottom": int(image.height - 1 - rows[-1]),
        "left": int(cols[0]),
        "right": int(image.width - 1 - cols[-1]),
    }


def auto_crop_border_image(image, target_color="#FFFFFF", tolerance=50, resize_back=True, resize_method="BILINEAR"):
    original_width, original_height = image.size
    target_rgb = _parse_hex_color(target_color)
    borders = find_first_non_color_borders(image, target_rgb, tolerance)

    if borders is None:
        return image.copy()

    left = borders["left"]
    top = borders["top"]
    right = original_width - borders["right"]
    bottom = original_height - borders["bottom"]

    if left >= right or top >= bottom:
        return image.copy()

    cropped = image.crop((left, top, right, bottom))
    if resize_back:
        cropped = cropped.resize((original_width, original_height), RESIZE_METHODS[resize_method])
    return cropped


class AutoCropBorder:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "target_color": ("STRING", {"default": "#FFFFFF"}),
                "tolerance": ("INT", {"default": 50, "min": 0, "max": 255, "display": "number"}),
                "resize_back": ("BOOLEAN", {"default": True}),
                "resize_method": (["LANCZOS", "BICUBIC", "NEAREST", "BILINEAR"], {"default": "BILINEAR"}),
                "mode": (["RGB", "RGBA"], {"default": "RGB"}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "auto_crop_border"
    CATEGORY = "ComfyUI-Light-Tool/image/Crop"
    DESCRIPTION = "Automatically crop target-color borders and optionally stretch the result back to original size"

    @staticmethod
    def auto_crop_border(image, target_color, tolerance, resize_back, resize_method, mode):
        img = tensor2pil(image).convert(mode)
        result_img = auto_crop_border_image(img, target_color, tolerance, resize_back, resize_method)
        return (pil2tensor(result_img),)


NODE_CLASS_MAPPINGS = {
    "Light-Tool: AutoCropBorder": AutoCropBorder
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Light-Tool: AutoCropBorder": "Light-Tool: Auto Crop Border"
}
