# -*- mode: python -*-
import sys
site_packages = [path for path in sys.path if path.rstrip("/\\").endswith('site-packages')]
print("site_packages:", site_packages)

block_cipher = None

added_files = [(site_packages_, ".") for site_packages_ in site_packages]

kwargs["datas"] = added_files

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
             cipher=block_cipher,
             **kwargs)
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
