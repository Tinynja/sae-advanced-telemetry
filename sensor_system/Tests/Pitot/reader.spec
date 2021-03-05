# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['reader.py'],
             pathex=['C:\\Users\\Amine\\OneDrive\\OneDrive - polymtl.ca\\1. SwishnFlick v4\\MEC8370 - Projet Intégrateur IV\\SAE_Advanced_Telemetry\\sensor_system\\Tests\\Pitot'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='reader',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='reader')
