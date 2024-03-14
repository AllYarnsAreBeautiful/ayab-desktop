from __future__ import annotations
from fbs_runtime.application_context.PySide6 import ApplicationContext

import sys
from os import path
import logging
from distutils.dir_util import copy_tree

from PySide6.QtCore import \
    Qt, QCoreApplication, QTranslator, QLocale, QSettings

from typing import TYPE_CHECKING, Any, cast
if TYPE_CHECKING: #TODO: why does mypy not resolve the absolute import correctly?
    from .ayab.ayab import GuiMain
    from .ayab import utils
    cached_property = property #HACK: from https://github.com/python/typing/discussions/1102#discussioncomment-2376328
else:  
    from ayab.ayab import GuiMain
    from ayab import utils
    from fbs_runtime.application_context.PySide6 import cached_property


class AppContext(ApplicationContext): #type: ignore # 1. Subclass ApplicationContext
    REPO = "AllYarnsAreBeautiful/ayab-desktop"

    def __init__(self)->None:
        self.configure_application()
        super().__init__()

    def configure_application(self)->None:
        # Remove Help Button
        if hasattr(Qt, 'AA_DisableWindowContextHelpButton'):
            QCoreApplication.setAttribute(
                Qt.AA_DisableWindowContextHelpButton, True)

    def run(self)->int:  # 2. Implement run()
        self.make_user_directory()
        self.configure_logger()
        self.install_translator()
        self.main_window.show()
        pkg = utils.package_version(self)
        tag = self.check_new_version(self.REPO)
        if tag != None and tag != pkg:
            url = "https://github.com/" + self.REPO + "/releases/tag/" + tag
            utils.display_blocking_popup(
               "<p>A new version of the AYAB desktop software has been released! You can download version <strong>" + tag + "</strong> using this link:<br/><br/><a href='" + url + "'>" + url + "</a></p>")
        return cast(int,self.app.exec())  # 3. End run() with this line

    def check_new_version(self, repo:str)->str:
        try:
            return utils.latest_version(repo)
        except Exception:
            return ""
            pass

    def make_user_directory(self)->None:
        self.userdata_path = path.expanduser(path.join("~", "AYAB"))
        # copy patterns into user directory
        copy_tree(self.get_resource("patterns"), self.userdata_path)

    def configure_logger(self)->None:
        logfile = path.join(self.userdata_path, "ayab_log.txt")
        logging.basicConfig(
            filename=logfile,
            level=logging.DEBUG,
            format='%(asctime)s %(name)-8s %(levelname)-8s %(message)s',
            datefmt='%y-%m-%d %H:%M:%S')
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        console.setFormatter(
            logging.Formatter(
                '%(asctime)s %(name)-8s %(levelname)-8s %(message)s'))
        logging.getLogger().addHandler(console)

    def install_translator(self)->None:
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
            logging.warning("Unable to load translation file " +
                            "for preferred language, using default locale")
            try:
                self.translator.load(QLocale.system(), "ayab_trans", "",
                                     lang_dir)
            except Exception:
                logging.warning("Unable to load translation file " +
                                "for default locale, using American English")
                self.translator.load("ayab_trans.en_US", lang_dir)
        except Exception:
            logging.error("Unable to load translation file")
            raise

        # install translator
        QCoreApplication.installTranslator(self.translator)

    @cached_property
    def main_window(self)->GuiMain:
        return GuiMain(self)


if __name__ == '__main__':
    appctxt = AppContext()  # 4. Instantiate the subclass
    exit_code = appctxt.run()  # 5. Invoke run()
    sys.exit(exit_code)
