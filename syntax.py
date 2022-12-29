import re
from PySide6 import QtCore, QtGui
import lexer


class JsonHighlighter (QtGui.QSyntaxHighlighter):
    """Syntax highlighter for the JSON format.
    """

    def __init__(self, parent: QtGui.QTextDocument) -> None:
        super().__init__(parent)

        self.mappings = {}
        self.setup_highlight()

    def setup_highlight(self):
        key_format = QtGui.QTextCharFormat()
        key_format.setForeground(QtCore.Qt.blue)
        self.mappings[lexer.TokenID.KEY] = key_format

        string_format = QtGui.QTextCharFormat()
        string_format.setForeground(QtCore.Qt.GlobalColor.darkGreen)
        self.mappings[lexer.TokenID.STRING] = string_format

        int_format = QtGui.QTextCharFormat()
        int_format.setForeground(QtCore.Qt.GlobalColor.cyan)
        self.mappings[lexer.TokenID.INT] = int_format

        null_format = QtGui.QTextCharFormat()
        null_format.setForeground(QtCore.Qt.GlobalColor.red)
        self.mappings[lexer.TokenID.NULL] = null_format

        bool_format = QtGui.QTextCharFormat()
        bool_format.setForeground(QtCore.Qt.GlobalColor.magenta)
        self.mappings[lexer.TokenID.BOOL] = bool_format

        separator_format = QtGui.QTextCharFormat()
        separator_format.setFontWeight(QtGui.QFont.Bold)
        separator_format.setForeground(QtCore.Qt.GlobalColor.lightGray)
        self.mappings[lexer.TokenID.COLON] = separator_format
        self.mappings[lexer.TokenID.COMMA] = separator_format
        self.mappings[lexer.TokenID.LEFT_SQ_BRACKET] = separator_format
        self.mappings[lexer.TokenID.RIGHT_SQ_BRACKET] = separator_format
        self.mappings[lexer.TokenID.LEFT_CURL_BRACKET] = separator_format
        self.mappings[lexer.TokenID.RIGHT_CURL_BRACKET] = separator_format

    def highlightBlock(self, text):
        """Apply syntax highlighting to the given block of text.
        """

        for token_id, start, end in lexer.lexer(text):
            fmt = self.mappings.get(token_id)
            if fmt is None:
                continue
            self.setFormat(start, end - start, fmt)

