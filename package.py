import os
import platform
import subprocess
import sys
from pathlib import Path

def build_app():
    """Build the application for the current platform."""
    system = platform.system()
    is_arm = platform.machine() == 'arm64'
    
    # Common PyInstaller arguments
    common_args = [
        '--name=CertGenerator',
        '--onefile',
        '--windowed',  # No console window
        '--clean',
        '--noconfirm',
        '--add-data=ui:ui',  # Include UI assets
        '--add-data=cert_generator:templates',  # Include templates
        '--icon=ui/icon.icns' if system == 'Darwin' else 'ui/icon.ico',
    ]
    
    if system == 'Darwin':  # macOS
        # Build .app bundle
        subprocess.run([
            'pyinstaller',
            *common_args,
            '--target-architecture=arm64' if is_arm else None,  # Only specify arch if on Apple Silicon
            '--osx-bundle-identifier=com.certgenerator.app',
            'main.py'
        ])
        
        # Move .app to dist folder
        app_path = Path('dist/CertGenerator.app')
        if app_path.exists():
            print(f"Successfully created {app_path}")
            
    elif system == 'Windows':
        # Build .exe
        subprocess.run([
            'pyinstaller',
            *common_args,
            'main.py'
        ])
        
        exe_path = Path('dist/CertGenerator.exe')
        if exe_path.exists():
            print(f"Successfully created {exe_path}")
    else:
        print(f"Unsupported platform: {system}")
        sys.exit(1)

if __name__ == '__main__':
    build_app() 