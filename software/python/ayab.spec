# -*- mode: python -*-
a = Analysis(['ayab/ayab.py'],
             pathex=['/home/tian/devel/ayab-apparat/software/python'],
             hiddenimports=['fysom', 'yapsy'],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='ayab',
          debug=True,
          strip=None,
          upx=False,
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
               strip=None,
               upx=False,
               name='ayab')
