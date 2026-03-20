#!/usr/bin/env python3
"""Optimize PNG images to reduce file size while maintaining quality."""

from PIL import Image
import os
from pathlib import Path

images_dir = Path(__file__).parent / "images"
target_size_kb = 200

for img_path in images_dir.glob("*.png"):
    print(f"Optimizing {img_path.name}...")
    
    # Open image
    img = Image.open(img_path)
    
    # Convert RGBA to RGB if needed
    if img.mode == 'RGBA':
        bg = Image.new('RGB', img.size, (255, 255, 255))
        bg.paste(img, mask=img.split()[3])
        img = bg
    
    # Resize to max 1024x1024 if larger
    if img.width > 1024 or img.height > 1024:
        img.thumbnail((1024, 1024), Image.Resampling.LANCZOS)
    
    # Save as JPEG with optimization
    output_path = img_path.with_suffix('.jpg')
    
    # Try different quality levels to hit target size
    for quality in [85, 75, 65, 55, 45]:
        img.save(output_path, 'JPEG', quality=quality, optimize=True)
        size_kb = output_path.stat().st_size / 1024
        
        if size_kb <= target_size_kb:
            print(f"  ✓ Saved as {output_path.name} ({size_kb:.1f}KB, quality={quality})")
            # Remove original PNG
            img_path.unlink()
            break
    else:
        print(f"  ⚠ Could not get below {target_size_kb}KB ({size_kb:.1f}KB)")

print("\nDone! Update index.html to reference .jpg instead of .png")
