# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['src/yzu_wlan/cli.py'],
    pathex=['src'],
    binaries=[],
    datas=[],
    hiddenimports=[
        'yzu_wlan',
        'yzu_wlan.cli',
        'yzu_wlan.config',
        'yzu_wlan.daemon',
        'yzu_wlan.portal',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='yzu-wlan',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
)
