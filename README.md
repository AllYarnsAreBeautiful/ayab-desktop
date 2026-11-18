# AYAB - All Yarns Are Beautiful

This is the GUI interface for AYAB.

For information on how to install the release version of the software, see
[http://manual.ayab-knitting.com](http://manual.ayab-knitting.com)

## Branching Model

**Development of the latest and upcoming features happens on the 'main' branch.** For each major release, a dedicated maintenance branch is created to manage bug fixes, security patches, and backporting for that specific release. These branches follow the naming convention <version>-maint (e.g. *0.95-maint*). This approach allows us to continue forward development while ensuring stability and long-term support for previous versions.

## Running from Source & Development

The AYAB desktop software runs using Python 3.11.

The development toolchain (Python and [uv](https://docs.astral.sh/uv/)) is managed by
[mise](https://mise.jdx.dev), and the Python dependencies are managed by uv:

* `mise.toml` pins the Python and uv versions.
* `pyproject.toml` declares the dependencies: the application dependencies, plus a `build`
  group (PyInstaller) and a `dev` group (pytest, mypy, pre-commit…).
* `uv.lock` pins the exact version of every package, including indirect dependencies. It is
  the single source of truth for dependency versions, locally and in CI.

### Platform-Specific Setup
<details>
    <summary>
        Linux
    </summary>

For flashing the firmware, avrdude has to be available on your system.
To build or run the application, you will also need the system libraries required by Qt 6; installing the Qt 6 development tools is a concise (if heavy-handed) way of bringing in these dependencies.

#### Debian/Ubuntu
```bash
    sudo apt install libasound2-dev avrdude qt6-tools-dev-tools build-essential
```
#### openSUSE
```bash
    sudo zypper install libasound2 alsa-devel avrdude qt6-tools-dev-tools build-essential
```
#### All Distributions

To be able to communicate with your Arduino, it might be necessary to add the
rights for USB communication by adding your user to some groups.
```bash
    sudo usermod -aG tty [userName]
    sudo usermod -aG dialout [userName]
```
</details>

<details>
    <summary>
        Windows
    </summary>

AYAB requires Windows version 10 or later.

Install [Git for Windows](https://git-scm.com/download/win), which also provides the
`bash` shell needed by `setup-environment.ps1`.

You will also need to download and install Perl from [https://www.perl.org/get.html](https://www.perl.org/get.html).
</details>

<details>
<summary>
macOS
</summary>

You can install Git using Homebrew:
```bash
    brew install git
```
You will also need the Xcode command line tools:
```bash
    xcode-select --install
```
Install python from [the official universal2 installer](https://www.python.org/ftp/python/3.11.8/python-3.11.8-macos11.pkg). (Conda does not produce universal binaries)  

If you encounter the pip `SSL:TLSV1_ALERT_PROTOCOL_VERSION` problem:
```bash
    curl https://bootstrap.pypa.io/get-pip.py | python
```
</details>

### Universal Setup Steps
Once platform-specific setup is complete, [install mise](https://mise.jdx.dev/getting-started.html)
and, optionally, [activate it in your shell](https://mise.jdx.dev/getting-started.html#activate-mise)
so that the right Python and the project virtual environment are picked up automatically
when you enter the repository.

Download the git repository:
```bash
    git clone https://github.com/AllYarnsAreBeautiful/ayab-desktop
    cd ayab-desktop
```
Install Python and uv, then set up the development environment:
```bash
    mise trust
    mise install
    mise run setup
```
`mise run setup` creates the virtual environment (`.venv`) with all dependencies from
`uv.lock`, converts the PySide6 `.ui` files, generates the translation files and installs
the [pre-commit](https://pre-commit.com/) git hooks.

Re-run `mise run generate` whenever a `.ui`, `.qrc` or translation file changes (e.g. after
a `git pull`).

Finally, you can start AYAB with
```bash
    mise exec -- uv run fbs run
```

If mise is activated in your shell, the `mise exec --` prefix is not needed (e.g. `uv sync`,
`uv run fbs run`).

Common tasks are defined in `mise.toml` (`mise tasks` lists them):
```bash
    mise run start    # run AYAB (regenerates the UI files first if needed)
    mise run ci       # lint, tests and type checking, as in the "Python Tests" workflow
    mise run build    # generate UI files, freeze the app and create the installer
```

### Managing dependencies

Edit dependencies with uv rather than by hand, so that `uv.lock` stays up to date:
```bash
    uv add <package>==<version>             # application dependency
    uv add --group dev <package>==<version> # development tool
    uv lock --upgrade-package <package>     # upgrade a single package
```
A pre-commit hook checks that `uv.lock` is up to date with `pyproject.toml` when you commit.

## CI/CD on GitHub

### Triggering a new build

A new build is triggered when a new tag is created, either starting with

* v (i.e. v1.0.0), or
* test (i.e. test230517)

Convention for the test-tag is to suffix the current date in the YYMMdd format. If there is already an existing test build for a single day, attach a letter.
The test tags and releases will be manually removed from time for a better overview.

The tag can be pushed from your local environment, or via the ["Draft a new Release"](https://github.com/AllYarnsAreBeautiful/ayab-desktop/releases/new) button on the GitHub website.

### Choosing the firmware release to be bundled with the build

The CI automatically downloads a given firmware release from the [ayab-firmware repo](https://github.com/AllYarnsAreBeautiful/ayab-firmware) and packs it into the Desktop release. The name of the firmware release is chosen in [this manifest file](https://github.com/AllYarnsAreBeautiful/ayab-desktop/blob/1.0.0-dev/src/main/resources/base/ayab/firmware/manifest.txt) in the ayab-desktop repo.

Whenever building from source, you should ensure that the firmware is available as a compiled hex file is available at `main/resources/base/ayab/firmware/firmware.hex`. You can either compile the firmware and upload it through other means (e.g. VSCode with PlatformIO), or compile and then drop it into the right path in the desktop directory, making it available for the flash through AYAB desktop.
