# -*- mode: python -*-
import os

spec_root = os.path.abspath(SPECPATH) + "/src"
block_cipher = None

a = Analysis(['src/main.py'],
             pathex=[spec_root],
             binaries=[],
             datas=[
                ('src/lib/nydus.ui', 'lib'),
                ('src/lib/UsernamesDialog.ui', 'lib'),
                ('src/lib/nydus.ico', 'lib'),
                ('src/lib/style.qss', 'lib'),
                ('VERSION', '.')
             ],
             hiddenimports=[
                'PyQt5.sip'
             ],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='nydus',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False,
          icon='src/lib/nydus.ico' )
