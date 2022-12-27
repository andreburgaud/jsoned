import re
from PySide6 import QtCore, QtGui


class JsonHighlighter (QtGui.QSyntaxHighlighter):
    """Syntax highlighter for the JSON format.
    """

    def __init__(self, parent: QtGui.QTextDocument) -> None:
        super().__init__(parent)

        self.mappings = {}
        self.setup_highlight()

    def setup_highlight(self):
        # name_format = QtGui.QTextCharFormat()
        # name_format.setForeground(QtCore.Qt.blue)
        # #pattern = r'"[^"\\]*(?:\\.[^"\\]*)*"(?=\s*:)'
        # pattern = r'"[^"\\]*(?:\\.[^"\\]*)*"\s*:'
        # self.mappings[pattern] = name_format

        string_format = QtGui.QTextCharFormat()
        string_format.setForeground(QtCore.Qt.GlobalColor.darkGreen)
        # pattern = r'"[^"\\](\\.[^"\\])*"(?!\s*:)'
        pattern = r'"[^"]*(\\.[^"\\]*)*"'
        self.mappings[pattern] = string_format

        # number_format = QtGui.QTextCharFormat()
        # number_format.setForeground(QtCore.Qt.red)
        # pattern = r'\b[+-]?[0-9]+(?:\.[0-9]+)?\b'
        # self.mappings[pattern] = number_format

    def highlightBlock(self, text):
        """Apply syntax highlighting to the given block of text.
        """

        for pattern, fmt in self.mappings.items():
            for match in re.finditer(pattern, text):
                start, end = match.span()
                self.setFormat(start, end - start, fmt)
