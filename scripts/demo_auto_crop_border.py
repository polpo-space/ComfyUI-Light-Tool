import os
import sys

from PIL import Image, ImageDraw


ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NODES_DIR = os.path.join(ROOT_DIR, "nodes")
TMP_DIR = os.path.join(ROOT_DIR, "tmp")
if NODES_DIR not in sys.path:
    sys.path.insert(0, NODES_DIR)

from image_auto_crop_border import auto_crop_border_image


def main():
    os.makedirs(TMP_DIR, exist_ok=True)

    source = Image.new("RGB", (640, 480), "white")
    draw = ImageDraw.Draw(source)
    draw.rectangle((140, 90, 539, 379), fill=(28, 132, 216))
    draw.ellipse((260, 160, 380, 280), fill=(255, 210, 80))

    cropped = auto_crop_border_image(source, "#FFFFFF", 50, resize_back=False, resize_method="BILINEAR")
    resized_back = auto_crop_border_image(source, "#FFFFFF", 50, resize_back=True, resize_method="BILINEAR")

    source_path = os.path.join(TMP_DIR, "auto_crop_border_source.png")
    cropped_path = os.path.join(TMP_DIR, "auto_crop_border_cropped.png")
    resized_path = os.path.join(TMP_DIR, "auto_crop_border_resized_back.png")

    source.save(source_path)
    cropped.save(cropped_path)
    resized_back.save(resized_path)

    print(f"source: {source_path}")
    print(f"cropped: {cropped_path} size={cropped.size}")
    print(f"resized_back: {resized_path} size={resized_back.size}")


if __name__ == "__main__":
    main()
