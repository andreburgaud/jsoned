# JSON Ed

JSON Editor and Validator written in Python with PySide6. 

I'm writing this tool mostly to play with PySide6.

![JSON Ed 2022-12-26 17-40-43](https://user-images.githubusercontent.com/6396088/209597735-dbbdf395-92eb-4673-8af3-208faeff9f4c.png)

## Notes

I will generate packages for the main platforms as the project evolves.

## Getting Started

### Starting jsoned in a development environment

#### Prepare initial environment

```bash
$ python3 -m venv .venv --prompt jsoned
$ . .venv/bin/activate
$ pip install --upgrade pip
$ pip install --upgrade setuptools
$ pip install -r requirements.txt
$ python jsoned.py
```

#### Subsequent usages

```bash
$ . .venv/bin/activate
$ python jsoned.py
```

## Development

In addition to the steps above, if you want to modify the UI, you may need to
use the Qt Designer and generate the corresponding Python code.

### Start Qt Designer

```bash
$ pyside6-designer jsoned.ui
```

### Generate the UI Python code

```bash
$ pyside6-uic jsoned.ui -o MainWindow.py
```

Only generate the file `MainWindow.py` from the UI file, `jsoned.ui`, and do
not modify the file manually.
