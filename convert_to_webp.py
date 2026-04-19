"""Konvertuje JPG/PNG fotky na WebP. Volitelně omezí maximální rozměr."""
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).parent
DIRS = ["Foto včely", "Příběh medu"]
MAX_DIM = 1600
QUALITY = 82

total_in = 0
total_out = 0
converted = 0

for d in DIRS:
    folder = ROOT / d
    if not folder.exists():
        print(f"SKIP: {d} (neexistuje)")
        continue
    for src in sorted(folder.iterdir()):
        if src.suffix.lower() not in (".jpg", ".jpeg", ".png"):
            continue
        dst = src.with_suffix(".webp")
        try:
            img = Image.open(src)
            img = ImageOps.exif_transpose(img)
            if img.mode in ("RGBA", "LA", "P"):
                img = img.convert("RGB")
            w, h = img.size
            scale = min(MAX_DIM / w, MAX_DIM / h, 1.0)
            if scale < 1.0:
                img = img.resize((int(w * scale), int(h * scale)), Image.LANCZOS)
            img.save(dst, "WEBP", quality=QUALITY, method=6)
            in_kb = src.stat().st_size / 1024
            out_kb = dst.stat().st_size / 1024
            total_in += in_kb
            total_out += out_kb
            converted += 1
            print(f"OK  {src.name:60} {in_kb:7.1f} KB -> {out_kb:7.1f} KB  ({out_kb/in_kb*100:.0f}%)")
        except Exception as e:
            print(f"ERR {src.name}: {e}")

print(f"\nHotovo. Souborů: {converted}, vstup: {total_in/1024:.1f} MB, výstup: {total_out/1024:.1f} MB, úspora: {(1-total_out/total_in)*100:.0f}%")
