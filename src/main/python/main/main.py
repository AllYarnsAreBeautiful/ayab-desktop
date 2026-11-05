from __future__ import annotations
from fbs_runtime.application_context.PySide6 import ApplicationContext

import sys
from os import path
import logging
from distutils.dir_util import copy_tree

from PySide6.QtCore import QCoreApplication, QTranslator, QLocale, QSettings

from typing import TYPE_CHECKING, cast


if TYPE_CHECKING:  # TODO: why does mypy not resolve the absolute import correctly?
    from main.ayab.ayab import GuiMain
    from main.ayab import utils
    from main.ayab.version_checker import VersionChecker

    # from https://github.com/python/typing/discussions/1102#discussioncomment-2376328
    cached_property = property
else:
    try:
        from main.ayab.ayab import GuiMain
        from main.ayab import utils
        from main.ayab.version_checker import VersionChecker
    except ImportError:  # 'fbs run' needs weird things.
        from ayab.ayab import GuiMain
        from ayab import utils
        from ayab.version_checker import VersionChecker
    from fbs_runtime.application_context.PySide6 import cached_property


class AppContext(ApplicationContext):  # type: ignore # 1. Subclass ApplicationContext
    _version_checker: VersionChecker

    def run(self) -> int:  # 2. Implement run()
        self.make_user_directory()
        self.configure_logger()
        self.install_translator()
        self.main_window.show()
        self._version_checker = VersionChecker(
            current_version=utils.package_version(self)
        )
        self._version_checker.start_background_check()
        return cast(int, self.app.exec())  # 3. End run() with this line

    def make_user_directory(self) -> None:
        self.userdata_path = path.expanduser(path.join("~", "AYAB"))
        # copy patterns into user directory
        copy_tree(self.get_resource("patterns"), self.userdata_path)

    def configure_logger(self) -> None:
        logfile = path.join(self.userdata_path, "ayab_log.txt")
        logging.basicConfig(
            filename=logfile,
            level=logging.INFO,
            format="%(asctime)s %(name)-8s %(levelname)-8s %(message)s",
            datefmt="%y-%m-%d %H:%M:%S",
        )
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        console.setFormatter(
            logging.Formatter("%(asctime)s %(name)-8s %(levelname)-8s %(message)s")
        )
        logging.getLogger().addHandler(console)

    def install_translator(self) -> None:
        # set constants for QSettings
        QCoreApplication.setOrganizationName("AYAB")
        QCoreApplication.setOrganizationDomain("ayab-knitting.com")
        QCoreApplication.setApplicationName("ayab")

        # choose language for translator
        self.translator = QTranslator()
        lang_dir = self.get_resource("ayab/translations")
        try:
            language = QSettings().value("language")
        except Exception:
            language = None
        try:
            self.translator.load(f"ayab_trans.{language}", lang_dir)
        except (TypeError, FileNotFoundError):
            logging.warning(
                "Unable to load translation file "
                + "for preferred language, using default locale"
            )
            try:
                self.translator.load(QLocale.system(), "ayab_trans", "", lang_dir)
            except Exception:
                logging.warning(
                    "Unable to load translation file "
                    + "for default locale, using American English"
                )
                self.translator.load("ayab_trans.en_US", lang_dir)
        except Exception:
            logging.error("Unable to load translation file")
            raise

        # install translator
        QCoreApplication.installTranslator(self.translator)

    @cached_property
    def main_window(self) -> GuiMain:
        return GuiMain(self)


if __name__ == "__main__":
    appctxt = AppContext()  # 4. Instantiate the subclass
    exit_code = appctxt.run()  # 5. Invoke run()
    sys.exit(exit_code)
