#!/usr/bin/env python3
"""Generate minimalist images for landing page via Alem.ai API."""

import requests
import time
from pathlib import Path

API_URL = "https://alem.ai/api/v1/image/generate"
OUTPUT_DIR = Path(__file__).parent / "images"

prompts = {
    "hero.png": "Minimalist 3D illustration: abstract flowing gradient waves in blue and purple, smooth clean surfaces, no text, no UI elements, modern corporate style, premium feel",
    
    "case-iftar.png": "Minimalist 3D icon: crescent moon and clock symbol, soft blue gradient, clean geometric shapes, no text, modern Islamic design, simple elegant",
    
    "case-whatsapp.png": "Minimalist 3D illustration: abstract chat bubbles or message flow, green gradient, smooth surfaces, no text, modern messaging concept, clean design",
    
    "case-2gis.png": "Minimalist 3D illustration: abstract map pin or location marker, orange gradient, smooth surfaces, no text, modern navigation concept, clean geometric",
    
    "case-blog.png": "Minimalist 3D illustration: abstract content or writing symbol, purple gradient, smooth surfaces, no text, modern publishing concept, elegant design"
}

def generate_image(prompt: str, output_path: Path) -> bool:
    """Generate image via Alem.ai API."""
    print(f"Generating: {output_path.name}...")
    print(f"Prompt: {prompt[:80]}...")
    
    try:
        response = requests.post(
            API_URL,
            json={"prompt": prompt, "size": "1024x1024"},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # Download image
            if "url" in data:
                img_response = requests.get(data["url"], timeout=30)
                if img_response.status_code == 200:
                    output_path.write_bytes(img_response.content)
                    size_kb = len(img_response.content) / 1024
                    print(f"  ✓ Saved {output_path.name} ({size_kb:.1f}KB)")
                    return True
            
            # Or direct image data
            elif "image" in data:
                output_path.write_bytes(data["image"])
                print(f"  ✓ Saved {output_path.name}")
                return True
        
        print(f"  ✗ API error: {response.status_code}")
        print(f"  Response: {response.text[:200]}")
        return False
        
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def main():
    """Generate all images."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    success_count = 0
    
    for filename, prompt in prompts.items():
        output_path = OUTPUT_DIR / filename
        
        if generate_image(prompt, output_path):
            success_count += 1
            time.sleep(2)  # Rate limiting
        else:
            print(f"  ⚠ Skipping {filename}")
    
    print(f"\n{'='*60}")
    print(f"Generated {success_count}/{len(prompts)} images")
    
    if success_count == len(prompts):
        print("\n✅ All images generated! Now optimizing...")
        return True
    else:
        print(f"\n⚠ {len(prompts) - success_count} images failed")
        return False

if __name__ == "__main__":
    main()
