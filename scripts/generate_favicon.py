"""Generate high-resolution PNG and multi-resolution ICO favicons for SpotForge."""

from pathlib import Path
from PIL import Image, ImageDraw


def generate_favicons():
    output_dir = Path("static")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Master canvas: 256x256
    size = 256
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Rounded rectangle background with gradient simulation
    radius = 64
    for y in range(size):
        ratio = y / size
        # Interpolate between purple (#9333ea: 147, 51, 234) and indigo (#4f46e5: 79, 70, 229)
        r = int(147 * (1 - ratio) + 79 * ratio)
        g = int(51 * (1 - ratio) + 70 * ratio)
        b = int(234 * (1 - ratio) + 229 * ratio)
        draw.line([(0, y), (size, y)], fill=(r, g, b, 255))

    # Create mask for rounded corners
    mask = Image.new("L", (size, size), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle([0, 0, size - 1, size - 1], radius=radius, fill=255)

    # Apply mask to gradient
    final_img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    final_img.paste(img, (0, 0), mask)
    draw = ImageDraw.Draw(final_img)

    # Draw Microphone geometry in white
    # Capsule: x in [100, 156], y in [56, 144], rx=28
    draw.rounded_rectangle([100, 56, 156, 144], radius=28, fill=(255, 255, 255, 50), outline=(255, 255, 255, 255), width=10)
    # Grill line
    draw.line([112, 92, 144, 92], fill=(255, 255, 255, 255), width=8)

    # U-shaped cradle: arc
    draw.arc([76, 76, 180, 172], start=0, end=180, fill=(255, 255, 255, 255), width=10)

    # Stand stem
    draw.line([128, 172, 128, 204], fill=(255, 255, 255, 255), width=10)
    # Base
    draw.line([96, 204, 160, 204], fill=(255, 255, 255, 255), width=10)

    # Save PNG
    png_path = output_dir / "favicon.png"
    final_img.save(png_path, format="PNG")
    print(f"Saved {png_path}")

    # Generate multi-size ICO: 16x16, 32x32, 48x48, 64x64
    ico_path = output_dir / "favicon.ico"
    sizes = [(16, 16), (32, 32), (48, 48), (64, 64)]
    final_img.save(ico_path, format="ICO", sizes=sizes)
    print(f"Saved multi-resolution {ico_path}")


if __name__ == "__main__":
    generate_favicons()
