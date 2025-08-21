from PIL import Image, ImageDraw, ImageFont
import os
import random

def generate_pixel_art(text, output_path="output.png", pixel_size=10):
    # Image size
    width, height = 500, 500
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)

    # Load font
    font = ImageFont.load_default()

    # Get text bounding box instead of textsize
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Center text
    x = (width - text_width) // 2
    y = (height - text_height) // 2

    # Draw text
    draw.text((x, y), text, fill="black", font=font)

    # Pixelate
    small = image.resize(
        (width // pixel_size, height // pixel_size),
        resample=Image.NEAREST
    )
    pixelated = small.resize(image.size, Image.NEAREST)

    # Save
    pixelated.save(output_path)
    print(f"✅ Pixel art saved at {output_path}")

if __name__ == "__main__":
    generate_pixel_art("Hello 🚀", "pixel_output.png", pixel_size=20)
