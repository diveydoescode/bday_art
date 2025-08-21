from PIL import Image, ImageDraw, ImageFont
import re

def remove_emojis(text):
    """Strip emojis if Pillow cannot render them."""
    return re.sub(r'[^\x00-\x7F]+', '', text)


class PixelArtGenerator:
    def __init__(self, pixel_size=8):
        self.pixel_size = pixel_size

    def generate_pixel_art(self, input_path, output_path, pixel_size, name="Friend"):
        try:
            # Open image
            img = Image.open(input_path).convert("RGB")

            # Pixelate
            small = img.resize(
                (img.width // pixel_size, img.height // pixel_size),
                resample=Image.NEAREST
            )
            pixelated = small.resize(img.size, Image.NEAREST)

            # Add birthday text
            draw = ImageDraw.Draw(pixelated)
            message = remove_emojis(f"🎂 Happy Birthday {name}! 🎉")

            try:
                font = ImageFont.truetype("arial.ttf", 40)
            except:
                font = ImageFont.load_default()

            # Use textbbox (new Pillow) instead of textsize
            bbox = draw.textbbox((0, 0), message, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

            x = (pixelated.width - text_width) // 2
            y = pixelated.height - text_height - 30

            # Shadow + text
            draw.text((x + 2, y + 2), message, font=font, fill="black")
            draw.text((x, y), message, font=font, fill="white")

            pixelated.save(output_path)
            return True

        except Exception as e:
            print(f"Error generating pixel art: {e}")
            return False
