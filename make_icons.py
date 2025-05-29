from PIL import Image
import subprocess
from pathlib import Path
import os

ui_dir = Path('ui')
png_path = ui_dir / 'icon.png'
icns_path = ui_dir / 'icon.icns'
ico_path = ui_dir / 'icon.ico'

# Open the PNG
img = Image.open(png_path).convert('RGBA')

# --- Create .icns (macOS) ---
if os.path.exists('/usr/bin/iconutil'):
    iconset_dir = ui_dir / 'icon.iconset'
    iconset_dir.mkdir(exist_ok=True)
    sizes = [16, 32, 64, 128, 256, 512, 1024]
    for size in sizes:
        resized = img.resize((size, size), Image.LANCZOS)
        resized.save(iconset_dir / f'icon_{size}x{size}.png')
        if size <= 512:
            resized2x = img.resize((size*2, size*2), Image.LANCZOS)
            resized2x.save(iconset_dir / f'icon_{size}x{size}@2x.png')
    subprocess.run(['iconutil', '-c', 'icns', str(iconset_dir), '-o', str(icns_path)])
    # Clean up
    for file in iconset_dir.glob('*'):
        file.unlink()
    iconset_dir.rmdir()

# --- Create .ico (Windows) ---
img.save(ico_path, format='ICO', sizes=[(16,16),(32,32),(48,48),(64,64),(128,128),(256,256)])

print(f"Icons created: {icns_path}, {ico_path}")
