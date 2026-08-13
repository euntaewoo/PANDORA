import os
import sys
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

source_dir = r"C:\Users\euntaewoo\Desktop\이미지번역워크스페이스\변역대상\02_아쿠아타이드 멀티퍼포스 토너 미스트\썸네일_logicallyskin_Aquatide-Multi-Purpose-Tone.png"
target_dir = os.path.join(source_dir, "썸네일")

os.makedirs(target_dir, exist_ok=True)

print(f"[START] Resizing images to 800x800 px...")
print(f"[INFO] Source folder: {source_dir}")
print(f"[INFO] Target folder: {target_dir}")

try:
    files = os.listdir(source_dir)
except Exception as e:
    print(f"[ERROR] Failed to read source directory: {e}")
    sys.exit(1)

image_extensions = ('.png', '.jpg', '.jpeg', '.jfif', '.webp', '.bmp')
targets = [f for f in files if f.lower().endswith(image_extensions)]

if not targets:
    print("[WARNING] No images found in source folder.")
    sys.exit(0)

success_count = 0
for filename in targets:
    in_path = os.path.join(source_dir, filename)
    out_path = os.path.join(target_dir, filename)
    
    print(f"  -> Resizing: {filename}...")
    try:
        with Image.open(in_path) as img:
            # Resize image to 800x800 using Lanczos resampling for high quality
            resized_img = img.resize((800, 800), Image.Resampling.LANCZOS)
            
            # Save to target folder with same extension/format
            resized_img.save(out_path, format=img.format)
            
            # Verify the output resolution immediately
            with Image.open(out_path) as verified_img:
                w, h = verified_img.size
                if w == 800 and h == 800:
                    print(f"    [SUCCESS] Resized to {w}x{h} px.")
                    success_count += 1
                else:
                    print(f"    [ERROR] Verified size mismatch: {w}x{h} px.")
    except Exception as e:
        print(f"    [ERROR] Failed to resize {filename}: {e}")

print(f"\n[FINISH] Resizing completed! Successfully resized {success_count}/{len(targets)} images.")
