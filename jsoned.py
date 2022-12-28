import json
import os
import pathlib
import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QLabel, QFileDialog
from MainWindow import Ui_MainWindow

import syntax


class MainWindow(QMainWindow, Ui_MainWindow):
    COL_ERROR = "red"
    COL_INFO = "black"
    TITLE = "JSON Ed"
    DEFAULT_FILE_NAME = "(Unnamed)"

    def __init__(self, app):
        super().__init__()
        self.app = app
        self.setupUi(self)
        self.file_name = ""
        self.set_default_file_name()
        self.modified = False
        self.set_title()
        syntax.JsonHighlighter(self.plainTextEdit.document())
        self.plainTextEdit.textChanged.connect(self.editor_text_changed)

        # Status bar (error notification)
        self.notification = QLabel()
        self.notification.setStyleSheet(f"QLabel {{ color: {MainWindow.COL_INFO} }}")
        self.statusbar.addPermanentWidget(self.notification)

        self.show()

        self.actionQuit.triggered.connect(self.quit)
        self.action_Format.triggered.connect(self.format)
        self.actionSave.triggered.connect(self.save)
        self.actionOpen.triggered.connect(self.open)
        self.actionNew.triggered.connect(self.new)

    def set_title(self) -> None:
        separator = '-'
        if self.modified:
            separator = '*'
        self.setWindowTitle(f"{self.file_name} {separator} {MainWindow.TITLE}")

    def set_default_file_name(self):
        self.file_name = MainWindow.DEFAULT_FILE_NAME

    def editor_text_changed(self):
        self.modified = True
        self.set_title()

    def new(self):
        if self.modified and self.plainTextEdit.toPlainText():
            reply = QMessageBox.question(self,
                                         'New',
                                         'Save changes to existing file before creating a new one?',
                                         QMessageBox.StandardButton.Cancel |
                                         QMessageBox.StandardButton.Yes |
                                         QMessageBox.StandardButton.No)

            if reply == QMessageBox.StandardButton.Cancel:
                return

            if reply == QMessageBox.StandardButton.Yes:
                self.save()

        self.plainTextEdit.setPlainText("")
        self.modified = True
        self.set_default_file_name()
        self.set_title()

    def open(self):
        result = QFileDialog.getOpenFileName(parent=self,
                                             caption="Open File",
                                             dir=str(pathlib.Path.home()),
                                             filter="JSON files (*.json)")
        file_name, _ = result
        self.file_name = file_name
        self.open_file()
        self.modified = False
        self.set_title()

    def open_file(self):
        with open(self.file_name, 'r') as f:
            data = f.read()
        if data:
            self.plainTextEdit.setPlainText(data)

    def notify_error(self, message):
        self.notification.setStyleSheet(f"QLabel {{ color: {MainWindow.COL_ERROR} }}")
        self.notification.setText(message)

    def notify_info(self, message):
        self.notification.setStyleSheet(f"QLabel {{ color: {MainWindow.COL_INFO} }}")
        self.notification.setText(message)

    def notify_clear(self):
        self.notification.setStyleSheet(f"QLabel {{ color: {MainWindow.COL_INFO} }}")
        self.notification.setText("")

    def save(self):
        file_name = self.file_name
        if os.path.exists(file_name):
            self.save_file()
            self.modified = False
            self.set_title()
        else:
            file_name = pathlib.Path.home() / self.file_name
            result = QFileDialog.getSaveFileName(parent=self,
                                                 caption="Save File",
                                                 dir=str(file_name),
                                                 filter="JSON files (*.json)")
            file_name, _ = result
            if file_name:
                self.file_name = file_name
                self.save_file()
                self.modified = False
                self.set_title()
            else:
                # save was canceled
                pass

    def save_file(self):
        with open(self.file_name, 'w') as f:
            f.write(self.plainTextEdit.toPlainText())

    def closeEvent(self, event):
        # Do any cleanup or check if file modified and not saved
        reply = QMessageBox.question(self, 'Quit', 'Are you sure you want to quit?',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
            self.app.quit()

        event.ignore()

    def quit(self, _):
        """Event triggered from the menu"""

        self.close()

    def format(self):
        """Format JSON code from the edit window"""

        self.notify_clear()
        json_text = self.plainTextEdit.toPlainText()
        try:
            json_dict = json.loads(json_text)
        except json.decoder.JSONDecodeError as err:
            self.notify_error(str(err))
        else:
            # json_fmt = json.dumps(json_dict, sort_keys=True, indent=2)
            json_fmt = json.dumps(json_dict, sort_keys=False, indent=2)
            self.plainTextEdit.setPlainText(json_fmt)
            self.notify_info("Formatting successful")


a = QApplication(sys.argv)
w = MainWindow(a)
a.exec()
