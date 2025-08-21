import os
import re
from PIL import Image, ImageDraw, ImageFont

# Utility: strip emojis if Pillow can't handle them
def remove_emojis(text: str) -> str:
    return re.sub(r'[^\x00-\x7F]+', '', text)

def generate_birthday_card(message: str, output_path: str = "birthday_card.png"):
    """
    Generates a simple birthday card with the given message.
    """

    # Ensure message is safe to render
    safe_message = remove_emojis(message)

    # Create a blank white image
    img = Image.new("RGB", (800, 400), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Load a font
    try:
        font = ImageFont.truetype("arial.ttf", 40)  # works locally if Arial exists
    except:
        font = ImageFont.load_default()  # fallback on Render

    # Center text
    text_width, text_height = draw.textsize(safe_message, font=font)
    position = ((800 - text_width) // 2, (400 - text_height) // 2)

    # Draw text in black
    draw.text(position, safe_message, font=font, fill="black")

    # Save the image
    img.save(output_path)
    return output_path

if __name__ == "__main__":
    # Example test run
    card_path = generate_birthday_card("🎂 Happy Birthday Shifa! 🎉")
    print(f"Generated card: {card_path}")
