"""
Generate a minimal test dataset for OneTrainer smoke testing.

Creates a small set of synthetic images with captions, plus a concepts.json
file ready to use with training presets (e.g. '#sd 1.5 LoRA (tiny-sd test).json').

Usage:
    python scripts/generate_test_dataset.py [--output-dir PATH] [--num-images N] [--resolution WxH]

Defaults:
    --output-dir  test_dataset/
    --num-images  10
    --resolution  256x256
"""

import argparse
import json
import random
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


CAPTIONS = [
    "a red circle on a blue background",
    "a green square on a white background",
    "a yellow triangle on a black background",
    "an orange rectangle on a gray background",
    "a purple ellipse on a pink background",
    "a cyan diamond on a dark background",
    "a white star on a red background",
    "a blue pentagon on a yellow background",
    "a magenta hexagon on a teal background",
    "a lime cross on a navy background",
    "a brown arrow on a beige background",
    "a gold ring on a silver background",
    "a crimson heart on a lavender background",
    "a turquoise spiral on a coral background",
    "an indigo wave on a cream background",
    "a scarlet dot on an olive background",
    "a chartreuse line on a maroon background",
    "a salmon zigzag on a slate background",
    "a periwinkle blob on a tan background",
    "a vermillion crescent on an ivory background",
]

COLOR_MAP = {
    "red": (255, 0, 0),
    "green": (0, 180, 0),
    "yellow": (255, 255, 0),
    "orange": (255, 165, 0),
    "purple": (128, 0, 128),
    "cyan": (0, 255, 255),
    "white": (255, 255, 255),
    "blue": (0, 0, 255),
    "magenta": (255, 0, 255),
    "lime": (0, 255, 0),
    "brown": (139, 69, 19),
    "gold": (255, 215, 0),
    "crimson": (220, 20, 60),
    "turquoise": (64, 224, 208),
    "indigo": (75, 0, 130),
    "scarlet": (255, 36, 0),
    "chartreuse": (127, 255, 0),
    "salmon": (250, 128, 114),
    "periwinkle": (204, 204, 255),
    "vermillion": (227, 66, 52),
}

BG_MAP = {
    "blue": (0, 0, 180),
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "gray": (128, 128, 128),
    "pink": (255, 192, 203),
    "dark": (30, 30, 30),
    "red": (180, 0, 0),
    "yellow": (255, 255, 0),
    "teal": (0, 128, 128),
    "navy": (0, 0, 128),
    "beige": (245, 245, 220),
    "silver": (192, 192, 192),
    "lavender": (230, 230, 250),
    "coral": (255, 127, 80),
    "cream": (255, 253, 208),
    "olive": (128, 128, 0),
    "maroon": (128, 0, 0),
    "slate": (112, 128, 144),
    "tan": (210, 180, 140),
    "ivory": (255, 255, 240),
}

SHAPES = [
    "circle", "square", "triangle", "rectangle", "ellipse",
    "diamond", "star", "pentagon", "hexagon", "cross",
    "arrow", "ring", "heart", "spiral", "wave",
    "dot", "line", "zigzag", "blob", "crescent",
]


def draw_shape(draw, shape, bbox, color):
    x0, y0, x1, y1 = bbox
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    w, h = x1 - x0, y1 - y0

    if shape == "circle":
        draw.ellipse(bbox, fill=color)
    elif shape == "square":
        side = min(w, h)
        draw.rectangle([cx - side // 2, cy - side // 2, cx + side // 2, cy + side // 2], fill=color)
    elif shape == "triangle":
        draw.polygon([(cx, y0), (x0, y1), (x1, y1)], fill=color)
    elif shape == "rectangle":
        draw.rectangle(bbox, fill=color)
    elif shape == "ellipse":
        draw.ellipse(bbox, fill=color)
    elif shape == "diamond":
        draw.polygon([(cx, y0), (x1, cy), (cx, y1), (x0, cy)], fill=color)
    elif shape == "star":
        # Simple 5-pointed star
        import math
        points = []
        for i in range(10):
            angle = math.pi / 2 + i * math.pi / 5
            r = min(w, h) // 2 if i % 2 == 0 else min(w, h) // 4
            points.append((cx + int(r * math.cos(angle)), cy - int(r * math.sin(angle))))
        draw.polygon(points, fill=color)
    elif shape == "pentagon":
        import math
        points = []
        for i in range(5):
            angle = math.pi / 2 + i * 2 * math.pi / 5
            r = min(w, h) // 2
            points.append((cx + int(r * math.cos(angle)), cy - int(r * math.sin(angle))))
        draw.polygon(points, fill=color)
    elif shape == "hexagon":
        import math
        points = []
        for i in range(6):
            angle = i * math.pi / 3
            r = min(w, h) // 2
            points.append((cx + int(r * math.cos(angle)), cy - int(r * math.sin(angle))))
        draw.polygon(points, fill=color)
    elif shape == "cross":
        t = min(w, h) // 6
        draw.rectangle([cx - t, y0, cx + t, y1], fill=color)
        draw.rectangle([x0, cy - t, x1, cy + t], fill=color)
    elif shape == "arrow":
        draw.polygon([(cx, y0), (x1, cy), (cx + w // 4, cy), (cx + w // 4, y1),
                       (cx - w // 4, y1), (cx - w // 4, cy), (x0, cy)], fill=color)
    elif shape == "ring":
        draw.ellipse(bbox, fill=color)
        inner_margin = min(w, h) // 4
        draw.ellipse([x0 + inner_margin, y0 + inner_margin, x1 - inner_margin, y1 - inner_margin], fill=(0, 0, 0, 0))
    elif shape == "heart":
        # Approximate heart
        draw.ellipse([x0, y0, cx, cy + h // 4], fill=color)
        draw.ellipse([cx, y0, x1, cy + h // 4], fill=color)
        draw.polygon([(x0, cy), (cx, y1), (x1, cy)], fill=color)
    elif shape == "spiral":
        # Draw concentric arcs as an approximation
        for i in range(5):
            r = min(w, h) // 2 - i * min(w, h) // 10
            if r > 0:
                draw.arc([cx - r, cy - r, cx + r, cy + r], i * 90, i * 90 + 270, fill=color, width=3)
    elif shape == "wave":
        import math
        points = []
        for px in range(x0, x1, 2):
            py = cy + int(h // 4 * math.sin((px - x0) / w * 4 * math.pi))
            points.append((px, py))
        if len(points) > 1:
            draw.line(points, fill=color, width=max(3, h // 16))
    elif shape == "dot":
        r = min(w, h) // 4
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)
    elif shape == "line":
        draw.line([x0, cy, x1, cy], fill=color, width=max(3, h // 8))
    elif shape == "zigzag":
        points = []
        segments = 6
        for i in range(segments + 1):
            px = x0 + i * w // segments
            py = y0 if i % 2 == 0 else y1
            points.append((px, py))
        draw.line(points, fill=color, width=max(2, h // 16))
    elif shape == "blob":
        # Random-ish blob via overlapping ellipses
        for _ in range(5):
            rx, ry = random.randint(x0, cx), random.randint(y0, cy)
            draw.ellipse([rx, ry, rx + w // 3, ry + h // 3], fill=color)
    elif shape == "crescent":
        draw.ellipse(bbox, fill=color)
        offset = w // 4
        draw.ellipse([x0 + offset, y0, x1 + offset, y1], fill=(0, 0, 0, 0))
    else:
        draw.ellipse(bbox, fill=color)


def generate_image(width, height, caption_index):
    """Generate a synthetic image matching the caption at caption_index."""
    caption = CAPTIONS[caption_index % len(CAPTIONS)]
    shape_name = SHAPES[caption_index % len(SHAPES)]

    # Pick colors from the maps based on caption index
    fg_colors = list(COLOR_MAP.values())
    bg_colors = list(BG_MAP.values())
    fg = fg_colors[caption_index % len(fg_colors)]
    bg = bg_colors[caption_index % len(bg_colors)]

    img = Image.new("RGB", (width, height), bg)
    draw = ImageDraw.Draw(img)

    margin = min(width, height) // 6
    bbox = (margin, margin, width - margin, height - margin)
    draw_shape(draw, shape_name, bbox, fg)

    return img, caption


def generate_concepts_json(dataset_dir, concept_name="test"):
    """Generate a minimal concepts.json pointing to the dataset directory."""
    concept = {
        "__version": 2,
        "image": {
            "__version": 0,
            "enable_crop_jitter": True,
            "enable_random_flip": True,
            "enable_fixed_flip": False,
            "enable_random_rotate": False,
            "enable_fixed_rotate": False,
            "random_rotate_max_angle": 0.0,
            "enable_random_brightness": False,
            "enable_fixed_brightness": False,
            "random_brightness_max_strength": 0.0,
            "enable_random_contrast": False,
            "enable_fixed_contrast": False,
            "random_contrast_max_strength": 0.0,
            "enable_random_saturation": False,
            "enable_fixed_saturation": False,
            "random_saturation_max_strength": 0.0,
            "enable_random_hue": False,
            "enable_fixed_hue": False,
            "random_hue_max_strength": 0.0,
            "enable_resolution_override": False,
            "resolution_override": "512",
            "enable_random_circular_mask_shrink": False,
            "enable_random_mask_rotate_crop": False,
        },
        "text": {
            "__version": 0,
            "prompt_source": "sample",
            "prompt_path": "",
            "enable_tag_shuffling": False,
            "tag_delimiter": ",",
            "keep_tags_count": 1,
            "tag_dropout_enable": False,
            "tag_dropout_mode": "FULL",
            "tag_dropout_probability": 0.0,
            "tag_dropout_special_tags_mode": "NONE",
            "tag_dropout_special_tags": "",
            "tag_dropout_special_tags_regex": False,
            "caps_randomize_enable": False,
            "caps_randomize_mode": "capslock, title, first, random",
            "caps_randomize_probability": 0.0,
            "caps_randomize_lowercase": False,
        },
        "name": concept_name,
        "path": str(Path(dataset_dir).resolve()),
        "seed": 42,
        "enabled": True,
        "type": "STANDARD",
        "include_subdirectories": False,
        "image_variations": 1,
        "text_variations": 1,
        "balancing": 1.0,
        "balancing_strategy": "REPEATS",
        "loss_weight": 1.0,
        "concept_stats": {},
    }
    return [concept]


def main():
    parser = argparse.ArgumentParser(description="Generate a test dataset for OneTrainer")
    parser.add_argument("--output-dir", type=str, default="test_dataset", help="Output directory for images and captions")
    parser.add_argument("--num-images", type=int, default=10, help="Number of images to generate")
    parser.add_argument("--resolution", type=str, default="256x256", help="Image resolution as WxH")
    args = parser.parse_args()

    width, height = (int(x) for x in args.resolution.split("x"))
    output_dir = Path(args.output_dir)
    images_dir = output_dir / "images"
    images_dir.mkdir(parents=True, exist_ok=True)

    random.seed(42)

    print(f"Generating {args.num_images} images at {width}x{height} in {images_dir}/")

    for i in range(args.num_images):
        img, caption = generate_image(width, height, i)
        img_path = images_dir / f"{i:04d}.png"
        txt_path = images_dir / f"{i:04d}.txt"

        img.save(img_path)
        txt_path.write_text(caption)

    # Write concepts.json
    concepts = generate_concepts_json(str(images_dir), concept_name="test-shapes")
    concepts_path = output_dir / "concepts.json"
    concepts_path.write_text(json.dumps(concepts, indent=4) + "\n")

    print(f"Created {args.num_images} images + captions in {images_dir}/")
    print(f"Created {concepts_path}")
    print()
    print("To use with training:")
    print(f'  1. Set concept_file_name to "{concepts_path.resolve()}"')
    print(f'  2. Or load the "#sd 1.5 LoRA (tiny-sd test)" preset and point it to this concepts file')


if __name__ == "__main__":
    main()
