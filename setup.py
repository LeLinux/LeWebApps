import subprocess as sb
sb.call(["sudo", "apt-get", "install", "python3-pip"])
sb.call(["pip3", "install", "pyqtdarktheme"])
sb.call(["pip3", "install", "pyside6"])
sb.call(["pip3", "install", "PySide6-Fluent-Widgets", "-i" , "https://pypi.org/simple/"])
