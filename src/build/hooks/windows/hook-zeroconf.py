from PyInstaller.utils.hooks import collect_submodules
# Collect all submodules within zeroconf
hiddenimports = collect_submodules('zeroconf')
