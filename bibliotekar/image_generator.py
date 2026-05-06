"""
entity_id=image_generator_module; type=module; state=initial

Module for generating images or infographics. Uses Pillow to create simple placeholder visuals when no external model is available. For advanced generation, integrate with OpenRouter or Stable Diffusion APIs. The ``create_placeholder`` function renders input text onto a white canvas as a fallback.
"""

from pathlib import Path
from typing import Tuple

from PIL import Image, ImageDraw, ImageFont  # type: ignore


def create_placeholder(text: str, size: Tuple[int, int], output_path: Path) -> Path:
    """Render the input text onto a blank image.

    entity_id=create_placeholder_function; type=function; state=initial

    Parameters
    ----------
    text: str
        Text to render on the image.
    size: tuple
        Image dimensions (width, height).
    output_path: Path
        Destination file path (PNG).

    Returns
    -------
    Path
        Path to generated image.
    """
    img = Image.new("RGB", size, color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 20)
    except Exception:
        font = ImageFont.load_default()
    margin = 10
    lines = text.split("\n")
    y = margin
    for line in lines:
        draw.text((margin, y), line, fill=(0, 0, 0), font=font)
        # Compute text height using bounding box to support recent Pillow versions
        try:
            # textbbox returns (left, top, right, bottom)
            bbox = draw.textbbox((0, 0), line, font=font)
            text_height = bbox[3] - bbox[1]
        except Exception:
            # Fallback: approximate line height via font metrics
            ascent, descent = font.getmetrics()
            text_height = ascent + descent
        y += text_height + 4
    img.save(str(output_path))
    return output_path