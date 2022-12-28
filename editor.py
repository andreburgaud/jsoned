from PySide6.QtWidgets import QWidget, QPlainTextEdit, QTextEdit
from PySide6.QtCore import QSize, QRect, Qt
from PySide6.QtGui import QColor, QPainter, QTextFormat, QFontDatabase

# Line numbers and highlight current line inspired from the following articles:
# - https://doc.qt.io/qt-5/qtwidgets-widgets-codeeditor-example.html
# - https://stackoverflow.com/questions/50074155/how-to-add-line-number-in-this-texteditor


class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(parent=editor)
        self.codeEditor = editor
        font = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        self.setFont(font)

    def sizeHint(self):
        return QSize(self.codeEditor.line_number_area_width(), 0)

    def paintEvent(self, event):
        self.codeEditor.line_number_area_paint_event(event)


class Editor(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color:lightyellow")
        font = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        self.setFont(font)

        self.lineNumberArea = LineNumberArea(self)
        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.cursorPositionChanged.connect(self.highlight_current_line)
        self.update_line_number_area_width()
        self.highlight_current_line()

    def line_number_area_paint_event(self, event):
        painter = QPainter(self.lineNumberArea)
        painter.fillRect(event.rect(), QColor(Qt.GlobalColor.lightGray).lighter(120))

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(Qt.GlobalColor.gray)
                # Start writing the line numbers to give enough margin between the border and the text
                painter.drawText(-5,
                                 top,
                                 self.lineNumberArea.width(),
                                 self.fontMetrics().height(),
                                 Qt.AlignRight, number)
            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            block_number += 1

    def line_number_area_width(self):
        # digits = len(str(self.blockCount()))
        digits = 7  # Fixed gutter size
        # TODO: improve calculation for gutter
        space = 3 + self.fontMetrics().horizontalAdvance('9')*digits
        return space

    def resizeEvent(self, event):
        QPlainTextEdit.resizeEvent(self, event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.line_number_area_width(), cr.height()))

    def update_line_number_area_width(self):
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    def highlight_current_line(self):
        extra_selections = []
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            line_color = QColor(Qt.GlobalColor.yellow).lighter(170)
            selection.format.setBackground(line_color)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extra_selections.append(selection)
        self.setExtraSelections(extra_selections)

    def update_line_number_area(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width()
