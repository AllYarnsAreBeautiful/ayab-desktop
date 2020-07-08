from fbs_runtime.application_context.PyQt5 import \
    ApplicationContext, cached_property

import sys
from os import path, mkdir
import logging
from PyQt5.QtCore import \
    Qt, QCoreApplication, QTranslator, QLocale, QSettings
from PyQt5.QtWidgets import QApplication

from ayab.ayab import GuiMain


class AppContext(ApplicationContext):  # 1. Subclass ApplicationContext
    def __init__(self, *args, **kwargs):
        self.configure_application()
        super().__init__(*args, **kwargs)

    def configure_application(self):
        # Fix PyQt5 for HiDPI screens
        if hasattr(Qt, 'AA_EnableHighDpiScaling'):
            QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
            QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
        # Remove Help Button
        if hasattr(Qt, 'AA_DisableWindowContextHelpButton'):
            QCoreApplication.setAttribute(Qt.AA_DisableWindowContextHelpButton,
                                          True)

    def run(self):  # 2. Implement run()
        self.make_user_directory()
        self.configure_logger()
        self.install_translator()
        self.main_window.show()
        return self.app.exec_()  # 3. End run() with this line

    def make_user_directory(self):
        self.userdata_path = path.expanduser(path.join("~", "AYAB"))
        if not path.isdir(self.userdata_path):
            mkdir(self.userdata_path)

    def configure_logger(self):
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

    def install_translator(self):
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
            self.translator.load("ayab_trans." + language, lang_dir)
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
    def main_window(self):
        return GuiMain(self)


if __name__ == '__main__':
    appctxt = AppContext()  # 4. Instantiate the subclass
    exit_code = appctxt.run()  # 5. Invoke run()
    sys.exit(exit_code)
