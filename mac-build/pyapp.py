#!/usr/bin/env python
import sys, os, os.path, stat

version = sys.argv[3]
bundleIdentifier = "com.ayab-knitting.AYAB"

script = os.path.abspath(sys.argv[1])
if not os.path.exists(script):
    print("\nFile "+script+" not found")
    Usage()
if os.path.splitext(script)[1].lower() != '.py':
    print("\nScript "+script+" does not have extension .py")
    Usage()

project = sys.argv[2]

# find the python application; must be an OS X app
pythonpath,top = os.path.split(os.path.realpath(sys.executable))
while top:
    if 'Resources' in pythonpath:
        pass
    elif os.path.exists(os.path.join(pythonpath,'Resources')):
        break
    pythonpath,top = os.path.split(pythonpath)
else:
    print("\nSorry, failed to find a Resources directory associated with "+str(sys.executable))
    sys.exit()
pythonapp = os.path.join(pythonpath,'Resources','Python.app','Contents','MacOS','Python')
if not os.path.exists(pythonapp): 
    print("\nSorry, failed to find a Python app in "+str(pythonapp))
    sys.exit()

apppath = os.path.abspath(os.path.join('.',project+".app"))
newpython =  os.path.join(apppath,"Contents","MacOS",project)
projectversion = project + " " + version
if os.path.exists(apppath):
    print("\nSorry, an app named "+project+" exists in this location ("+str(apppath)+")")
    sys.exit()

os.makedirs(os.path.join(apppath,"Contents","MacOS"))

f = open(os.path.join(apppath,"Contents","Info.plist"), "w")
f.write('''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleDevelopmentRegion</key>
    <string>English</string>
    <key>CFBundleExecutable</key>
    <string>main.sh</string>
    <key>CFBundleGetInfoString</key>
    <string>{:}</string>
    <key>CFBundleIconFile</key>
    <string>app.icns</string>
    <key>CFBundleIdentifier</key>
    <string>{:}</string>
    <key>CFBundleInfoDictionaryVersion</key>
    <string>6.0</string>
    <key>CFBundleName</key>
    <string>{:}</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>{:}</string>
    <key>CFBundleSignature</key>
    <string>????</string>
    <key>CFBundleVersion</key>
    <string>{:}</string>
    <key>NSAppleScriptEnabled</key>
    <string>YES</string>
    <key>NSMainNibFile</key>
    <string>MainMenu</string>
    <key>NSPrincipalClass</key>
    <string>NSApplication</string>
</dict>
</plist>
'''.format(projectversion, bundleIdentifier, project, projectversion, version)
    )
f.close()

# not sure what this file does
f = open(os.path.join(apppath,'Contents','PkgInfo'), "w")
f.write("APPL????")
f.close()
# create a link to the python app, but named to match the project
os.symlink(pythonapp,newpython)
# create a script that launches python with the requested app
shell = os.path.join(apppath,"Contents","MacOS","main.sh")
# create a short shell script
f = open(shell, "w")
f.write('#!/bin/sh\nexec "'+newpython+'" "'+script+'"\n')
f.close()
os.chmod(shell, os.stat(shell).st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
