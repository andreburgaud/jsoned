# default recipe (this list)
default:
    @just --list

# Start the editor
run:
    python jsoned.py

# Start the Qt Designer
designer:
    pyside6-designer jsoned.ui

# Generate Python code from UI file
uic:
    pyside6-uic jsoned.ui -o MainWindow.py