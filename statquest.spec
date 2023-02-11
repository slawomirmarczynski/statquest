# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

import os
my_prefix = os.getenv('CONDA_PREFIX')
my_site = my_prefix + r'\Lib\site-packages'
my_pcg = r'\ydata_profiling\report\presentation\flavours\html\templates'

added_files = [
    (my_site + my_pcg, '.' + my_pcg)
]

a = Analysis(
    ['statquest\\statquest_main.py'],
    pathex=['statquest'],
    binaries=[],
    datas=added_files,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='statquest',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # was True
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='statquest',
)
