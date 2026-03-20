#!/usr/bin/env python3
"""Optimize new PNG images to JPEG <200KB."""

from PIL import Image
from pathlib import Path

images_dir = Path(__file__).parent / "images"
target_size_kb = 200

new_images = list(images_dir.glob("*-new.png"))

if not new_images:
    print("No new images found")
    exit(1)

print(f"Found {len(new_images)} images to optimize\n")

for png_path in new_images:
    print(f"Optimizing {png_path.name}...")
    
    # Open and convert RGBA to RGB
    img = Image.open(png_path)
    if img.mode == 'RGBA':
        bg = Image.new('RGB', img.size, (255, 255, 255))
        bg.paste(img, mask=img.split()[3])
        img = bg
    
    # Resize if needed
    if img.width > 1024 or img.height > 1024:
        img.thumbnail((1024, 1024), Image.Resampling.LANCZOS)
    
    # Output path (replace -new.png with .jpg)
    jpg_name = png_path.name.replace('-new.png', '.jpg')
    jpg_path = images_dir / jpg_name
    
    # Try different quality levels
    for quality in [85, 75, 65, 55, 45]:
        img.save(jpg_path, 'JPEG', quality=quality, optimize=True)
        size_kb = jpg_path.stat().st_size / 1024
        
        if size_kb <= target_size_kb:
            print(f"  ✓ {jpg_name} ({size_kb:.1f}KB, quality={quality})")
            # Remove PNG
            png_path.unlink()
            break
    else:
        print(f"  ⚠ Could not get below {target_size_kb}KB ({size_kb:.1f}KB)")

print("\n✅ All images optimized!")
