import sys, qdarkstyle, os, ctypes, requests, qdarkstyle.pyqt5_style_rc
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QFile, QTextStream
from ui.MainWindow import MainWindow
from support.plugins.PluginCollection import PluginCollection
from support.Worker import Worker
from support.Logger import Logger

# needed for SceneSwitcher on linux with pyinstaller
from array import array

# needed for windows with pyinstaller
try:
    from ctypes import wintypes
except:
    pass

def main():
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    logger = Logger(os.path.abspath("."))
    sys.stdout = logger
    sys.stderr = logger

    try:
        app = QApplication(sys.argv)
        app.setWindowIcon(QIcon(base_path + '/lib/nydus.ico'))
        app.setStyleSheet(get_stylesheet(base_path))

        # set up nydus
        worker = Worker()
        worker.start()
        plugins = PluginCollection(worker)
        mw = MainWindow(base_path, plugins)

        # check for updates
        try:
            updates = check_for_updates(base_path)
            if updates:
                mw.updates(updates['html_url'], updates['body'])
        except Exception as e:
            logger.log("[Core] Couldnt check for updates: [%s] %s" % (e.__class__.__name__, str(e)))

        sys.exit(app.exec_())

    except Exception as e:
        logger.log("[Core] Fatal error: " + str(e))
        logger.dump()
        sys.exit(1)

def get_stylesheet(base_path):
    f = QFile(base_path + "/lib/style.qss")
    if f.exists():
        f.open(QFile.ReadOnly | QFile.Text)
        ts = QTextStream(f)
        return ts.readAll()
    return qdarkstyle.load_stylesheet_pyqt5()

def check_for_updates(base_path):
    with open("%s/VERSION" % base_path, "r") as f:
        _VERSION = tuple(f.read().rstrip(os.linesep).split("."))
    r = requests.get('https://api.github.com/repos/leigholiver/nydus/releases/latest')
    if r.status_code == "200" and tuple(response['tag_name'].split(".")) > _VERSION:
        response = r.json()
        return response
    return False

if __name__ == "__main__":
    main()
