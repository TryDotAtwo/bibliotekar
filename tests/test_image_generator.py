"""
Tests for image generation module. Ensures placeholder images are created with the requested size.
"""

from pathlib import Path

from PIL import Image  # type: ignore

from bibliotekar.image_generator import create_placeholder


def test_create_placeholder(tmp_path: Path) -> None:
    text = "Demo Placeholder"
    size = (200, 100)
    img_path = tmp_path / "placeholder.png"
    create_placeholder(text, size, img_path)
    assert img_path.exists()
    # Load image to verify dimensions
    with Image.open(str(img_path)) as img:
        assert img.size == size