# PyInstaller spec for the Linux itch.io build.
#
# Build with: uv run pyinstaller pacman.spec --noconfirm
# Full packaging steps (assets, config, instructions, zip): see the
# "Packaging & Itch.io" section of README.md.
#
# Game assets and the default config are intentionally NOT bundled as
# PyInstaller `datas`: the game loads them through plain relative paths
# (e.g. "assets/background/..."), resolved against the current working
# directory, so they are copied next to the built executable by hand
# instead, matching the source tree layout exactly.

a = Analysis(
    ['pac-man.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
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
    [],
    exclude_binaries=True,
    name='pacman',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='pacman',
)
