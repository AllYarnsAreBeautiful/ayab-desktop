# -*- mode: python -*-
import sys

block_cipher = None

a = Analysis(['ayab/ayab.py'],
             pathex=['./ayab'],
             hiddenimports=[],
             binaries=[],
             datas=[],
             hookspath=hookspath(),
             runtime_hooks=runtime_hooks(),
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='AYAB',
          debug=True,
          strip=False,
          upx=True,
          console=True )

# Include all files in plugins folder
plugin_tree = Tree('ayab/plugins', prefix = 'plugins')
# add README to that TOC for convenience
plugin_tree += [('README.md', './README.md', 'DATA')]

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               plugin_tree,
               strip=False,
               upx=True,
               name='AYAB')

app = BUNDLE(coll,
             name='AYAB.app',
             icon=None,
             bundle_identifier="com.ayab-knitting.AYAB")
