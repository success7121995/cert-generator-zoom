# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('ui/assets', 'assets'),
        ('ui/style.qss', 'ui'),
        ('excel_reader', 'excel_reader'),
        ('cert_generator', 'cert_generator'),
        ('ui', 'ui'),
        ('main.py', '.'),
    ],
    hiddenimports=[
        'PyQt6',
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
        'pandas',
        'openpyxl',
        'docx',
        'PIL',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='CertGenerator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch='arm64',
    codesign_identity=None,
    entitlements_file=None,
    icon=['ui/icon.icns'],
)
app = BUNDLE(
    exe,
    name='CertGenerator.app',
    icon='ui/icon.icns',
    bundle_identifier='com.certgenerator.app',
)
