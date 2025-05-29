# Certificate Generator

A PyQt5 desktop application for generating certificates.

## Building the Application

### Prerequisites

1. Install Python 3.8 or later
2. Install required packages:
   ```bash
   pip install -r requirements.txt
   pip install pyinstaller
   ```

### Required Icons

Before building, ensure you have the following icon files:
- `ui/icon.icns` for macOS
- `ui/icon.ico` for Windows

You can create these from a PNG file using:
- macOS: Use Icon Composer or online converters
- Windows: Use online converters or icon editors

### Building on macOS

1. Run the build script:
   ```bash
   python package.py
   ```

2. The `.app` bundle will be created in the `dist` folder.

### Building on Windows

1. Run the build script:
   ```bash
   python package.py
   ```

2. The `.exe` file will be created in the `dist` folder.

### Building for Windows on macOS

To build a Windows executable on macOS, you'll need to:

1. Install Wine:
   ```bash
   brew install wine
   ```

2. Install Python for Windows through Wine:
   ```bash
   winetricks python39
   ```

3. Install required packages in the Windows Python environment:
   ```bash
   wine python -m pip install -r requirements.txt
   wine python -m pip install pyinstaller
   ```

4. Run the build script:
   ```bash
   wine python package.py
   ```

## GitHub Actions Build

For automated Windows builds, you can use GitHub Actions. Create a workflow file at `.github/workflows/build.yml`:

```yaml
name: Build Windows Executable

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: windows-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pyinstaller
    - name: Build executable
      run: python package.py
    - name: Upload artifact
      uses: actions/upload-artifact@v2
      with:
        name: windows-executable
        path: dist/CertGenerator.exe
```

## Notes

- The application is built as a single executable file
- All assets (images, templates) are included in the package
- No console window will appear when running the application
- The macOS build supports both Intel and Apple Silicon processors # cert-generator-zoom
