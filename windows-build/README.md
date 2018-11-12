# windows-build

To build a binary from the Python script files, use PyInstaller (pip install pyinstaller) inside the virtualenv:

    cd ayab-desktop
    venv\Scripts\activate
    python3 -m fbs freeze

This will generate a standalone build inside target/AYAB
To build the NSIS installer, run 
    
    python3 -m fbs installer

(NSIS must be on the Windows PATH)

## Win10 Build dependencies

* vcredist packages
  * https://www.microsoft.com/en-us/download/confirmation.aspx?id=26999
  * https://www.microsoft.com/en-us/download/confirmation.aspx?id=30679
  * https://www.microsoft.com/en-us/download/confirmation.aspx?id=48145
  * https://developer.microsoft.com/en-us/windows/downloads/windows-10-sdk

* git for windows (https://git-scm.com/download/win)
* python 3.5.3 (64 bit) (https://www.python.org/downloads/release/python-353/)
* NSIS http://nsis.sourceforge.net/Download
* gitlab-runner (https://docs.gitlab.com/runner/install/windows.html)

## Settings

* Add to Path
  * C:\Programs and Files\Git\bin\
  * NSIS
  * %SystemRoot%/SysWOW64

* config.toml
  * executor = "shell"
  * shell = "bash"
  * build_dir = "/c/gitlab-runner/builds/"
  * builds_cache = "/c/gitlab-runner/cache/"

## Gitlab Runner Call
C:\Program Files\Git\bin\bash.exe -c "/c/gitlab-runner/gitlab-runner.exe run --working-directory /c/gitlab-runner --config /c/gitlab-runner/config.toml --service gitlab-runner --syslog"
