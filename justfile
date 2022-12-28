VERSION := "0.2.0"

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

# Push and tag the code to Github
git-push: version
    @git push
    @git tag -a {{VERSION}} -m "Version {{VERSION}}"
    @git push origin --tags

# Display the version
version:
    @echo "version {{VERSION}}"