import sys

import qdarktheme
from PySide6 import QtWidgets, QtGui, QtCore
import qfluentwidgets  as qfw
import os
import shutil

import subprocess as sb
import desktop_template as dtemplate

class QDoubleButton(QtWidgets.QToolButton):
    right_clicked = QtCore.Signal()
    left_clicked = QtCore.Signal()
    double_clicked = QtCore.Signal()

    def __init__(self, *args, **kwargs):
        super(QDoubleButton, self).__init__(*args, **kwargs)

        self.timer = QtCore.QTimer()
        self.timer.setSingleShot(True)
        self.timer.setInterval(250)
        self.timer.timeout.connect(self.timeout)

        self.is_double = False
        self.is_left_click = True

        self.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.MouseButtonPress:
            if not self.timer.isActive():
                self.timer.start()

            self.is_left_click = False
            if event.button() == QtCore.Qt.LeftButton:
                self.is_left_click = True

            return True

        elif event.type() == QtCore.QEvent.MouseButtonDblClick:
            if event.button() == QtCore.Qt.LeftButton:
                self.is_double = True
                return True

        return False

    def timeout(self):
        if self.is_double:
            self.double_clicked.emit()
        else:
            if self.is_left_click:
                self.left_clicked.emit()
            else:
                self.right_clicked.emit()

        self.is_double = False

    def left_click_event(self):
        print('left clicked')

    def right_click_event(self):
        print('right clicked')

    def double_click_event(self):
        print('double clicked')

class DeleteApp(QtWidgets.QMainWindow):
    def __init__(self, parent = None, name = None):
        super().__init__()

        self.setFixedWidth(400)
        self.setFixedHeight(130)

        self.name = name
        self.parent = parent

        self.setWindowTitle(self.name)

        self.cund_group = QtWidgets.QGroupBox(self)
        self.cund_vbox = QtWidgets.QVBoxLayout()

        self.app_name = QtWidgets.QLabel(text = self.name)

        self.delete_n_cancel_group_box = QtWidgets.QGroupBox()
        self.delete_n_cancel_hbox = QtWidgets.QHBoxLayout()

        self.delete_n_cancel_group_box.setLayout(self.delete_n_cancel_hbox)

        self.cancel = QtWidgets.QPushButton(text = "Cancel")
        self.cancel.setStyleSheet("QPushButton{color : white;}")
        self.cancel.clicked.connect(self.Cancel)

        self.delete = QtWidgets.QPushButton(text = "Delete")
        self.delete.setStyleSheet("QPushButton{color : red;}")
        self.delete.clicked.connect(self.Delete)

        self.delete_n_cancel_hbox.addWidget(self.delete)
        self.delete_n_cancel_hbox.addWidget(self.cancel)

        self.cund_vbox.addWidget(self.app_name)
        self.cund_vbox.addWidget(self.delete_n_cancel_group_box)

        self.cund_group.setLayout(self.cund_vbox)

        self.setCentralWidget(self.cund_group)

    def Delete(self):
        os.remove("./icons/" + self.name)
        os.remove("./apps/" + self.name + ".py")
        os.remove(os.path.expanduser('~') + "/.local/share/applications/" + self.name + ".desktop")
        self.parent.appsRefresh()
        self.hide()


    def Cancel(self):
        self.hide()


class LeWebApps(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.global_icon_name = None

        self.setWindowTitle("LeWebApps")


        self.main_group = QtWidgets.QGroupBox(self)

        self.main_vbox = QtWidgets.QVBoxLayout()

        self.main_group.setLayout(self.main_vbox)

        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(1)
        self.installed_apps_flow_layout = qfw.FlowLayout(needAni = 1)

        self.appsRefresh()

        self.installed_apps_group = QtWidgets.QGroupBox()
        self.installed_apps_group.setLayout(self.installed_apps_flow_layout)

        self.scroll_area.setWidget(self.installed_apps_group)

        self.new_app_url_label = QtWidgets.QLabel(text = "URL")
        #self.new_app_url_label.setStyleSheet("""QLabel{font-size: 18px;}""")

        self.new_app_group = QtWidgets.QGroupBox(self)

        self.new_app_hbox = QtWidgets.QHBoxLayout()

        self.new_app_group.setLayout(self.new_app_hbox)

        self.new_app_name_label = QtWidgets.QLabel(text = "App name")
        self.new_app_name_line_edit = QtWidgets.QLineEdit()

        self.new_app_url_line_edit = QtWidgets.QLineEdit()
        self.new_app_browse_icon = QtWidgets.QPushButton(text = "Icon browse...")
        self.new_app_browse_icon.clicked.connect(self.openIcon)
        self.new_app_button = QtWidgets.QPushButton(text = "+")
        self.new_app_button.clicked.connect(self.createApp)
        self.new_app_hbox.addWidget(self.new_app_url_line_edit)
        self.new_app_hbox.addWidget(self.new_app_browse_icon)
        #self.new_app_hbox.addWidget(self.new_app_button)

        self.main_vbox.addWidget(self.new_app_name_label)
        self.main_vbox.addWidget(self.new_app_name_line_edit)
        self.main_vbox.addWidget(self.new_app_url_label)
        self.main_vbox.addWidget(self.new_app_group)
        self.main_vbox.addWidget(self.new_app_button)
        self.main_vbox.addWidget(self.scroll_area)

        self.setCentralWidget(self.main_group)

    def openIcon(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', "~/", "Image Files(*.png *.jpg *.bmp *.jpeg *.svg)")
        print(fname[0])
        self.global_icon_name = fname[0]
        #shutil.copyfile(fname[0], "./icons/" + "test")
        self.new_app_browse_icon.setIcon(QtGui.QIcon(fname[0]))
        self.new_app_browse_icon.setIconSize(QtCore.QSize(30, 30))
        self.new_app_browse_icon.setText("")

    def createApp(self):
        url = self.new_app_url_line_edit.text()
        template = f'''import subprocess as sb
sb.call(["surf", "{url}"])
            '''
        shutil.copyfile(self.global_icon_name, "./icons/" + self.new_app_name_line_edit.text())

        with open("apps/" + self.new_app_name_line_edit.text() + ".py", "w") as new_app:
            new_app.write(template)

        pre_desktop_file = dtemplate.template.split("{separate}")
        print(pre_desktop_file)
        desktop_file = pre_desktop_file[0] + self.new_app_name_line_edit.text()
        desktop_file += pre_desktop_file[1] + "python3 " +  os.path.abspath("./apps/" + self.new_app_name_line_edit.text() + ".py")
        desktop_file += pre_desktop_file[2] + os.path.abspath("./icons/" + self.new_app_name_line_edit.text())
        desktop_file += pre_desktop_file[3]
        print(desktop_file)

        with open(os.path.expanduser('~') + "/.local/share/applications/" + self.new_app_name_line_edit.text() + ".desktop", "w") as new_desktop:
            new_desktop.write(desktop_file)

        sb.call(["xdg-desktop-menu", "install", os.path.expanduser('~') + "/.local/share/applications/" + self.new_app_name_line_edit.text() + ".desktop"])
        self.appsRefresh()

    def appsRefresh(self):
        self.installed_apps_flow_layout.takeAllWidgets()

        self.active_apps = os.listdir("./apps/")
        print(self.active_apps)

        for i in self.active_apps:
            new_button = QtWidgets.QToolButton()
            new_button.setText(i[:-3])
            new_button.setIcon(QtGui.QIcon("./icons/" + i[:-3]))
            new_button.setIconSize(QtCore.QSize(40, 40))
            new_button.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
            new_button.setStyleSheet("""QToolButton{margin-left: 10px;}""")
            new_button.clicked.connect(self.openAppMenuLambda(i[:-3]))
            self.installed_apps_flow_layout.addWidget(new_button)

    def openAppMenu(self, name):
        self.menu = DeleteApp(self, name = name)
        self.menu.show()

    def openAppMenuLambda(self, name):
        return lambda: self.openAppMenu(name)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])


    qdarktheme.setup_theme()

    app.setFont(QtGui.QFont("Ubuntu Mono"))

    lefiles = LeWebApps()
    lefiles.resize(800, 600)
    lefiles.show()

    sys.exit(app.exec())
