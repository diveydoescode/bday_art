import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os
from typing import Tuple, List
import random
import re  # 👈 Added

def remove_emojis(text: str) -> str:
    """Strip emojis / non-ASCII chars so Pillow doesn't crash"""
    return re.sub(r'[^\x00-\x7F]+', '', text)

class PixelArtGenerator:
    def __init__(self, pixel_size: int = 8):
        """Initialize pixel art generator with customizable pixel size"""
        self.pixel_size = pixel_size
        
        # Kawaii/cute color palette inspired by the cat image
        self.cute_palette = [
            (45, 45, 55),
            (75, 75, 95),
            (120, 85, 140),
            (160, 120, 180),
            (255, 220, 180),
            (255, 180, 120),
            (255, 140, 140),
            (140, 200, 120),
            (100, 180, 100),
            (180, 220, 255),
            (255, 255, 255),
            (255, 200, 0),
        ]
        
    # ... keep reduce_colors and pixelate_image unchanged ...

    def add_pixel_birthday_message(self, image: Image.Image, name: str = "Afshah") -> Image.Image:
        """Add cute pixel-style birthday message"""
        draw = ImageDraw.Draw(image)
        width, height = image.size
        
        # Raw message with emojis
        raw_message = f"Happy Birthday {name}! 🎂"
        # Strip emojis so Pillow won't break
        message = remove_emojis(raw_message)
        
        try:
            font_size = max(12, width // 40)
            font = ImageFont.load_default()
        except:
            font = ImageFont.load_default()
        
        bbox = draw.textbbox((0, 0), message, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        margin = 20
        bg_x = (width - text_width) // 2 - margin
        bg_y = height - text_height - margin * 2
        bg_width = text_width + margin * 2
        bg_height = text_height + margin
        
        self.draw_pixel_rect(draw, bg_x, bg_y, bg_width, bg_height, 
                             fill_color=(255, 255, 255, 200), 
                             border_color=(45, 45, 55))
        
        text_x = bg_x + margin
        text_y = bg_y + margin // 2
        
        # Outline
        for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (1, 0), (0, -1), (0, 1)]:
            draw.text((text_x + dx, text_y + dy), message, font=font, fill=(45, 45, 55))
        
        # Main text
        draw.text((text_x, text_y), message, font=font, fill=(255, 140, 140))
        
        return image
