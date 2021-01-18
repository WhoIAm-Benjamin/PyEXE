import sys
from subprocess import DEVNULL, PIPE, STDOUT, Popen

from PySide2.QtCore import Qt
from PySide2.QtWidgets import (QApplication, QCheckBox, QLineEdit, QPushButton,
                               QTextEdit, QWidget, QGridLayout)

from style import Style


# noinspection PyPep8Naming
class PathEdit(QLineEdit):
    def __init__(self, text='', parent=None):
        super(PathEdit, self).__init__(text, parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super(PathEdit, self).dragEnterEvent(event)

    def dragMoveEvent(self, event):
        super(PathEdit, self).dragMoveEvent(event)

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                self.setText(url.path())
            event.acceptProposedAction()
        else:
            super(PathEdit, self).dropEvent(event)


# noinspection PyPep8Naming,PyArgumentList
class MyWidget(QWidget):
    # noinspection PyUnresolvedReferences
    def __init__(self):
        super().__init__()
        self.console = QTextEdit()

        self.ch_console = QCheckBox("Console/No console")

        self.ch_dir = QCheckBox("One File/Folder")

        self.ch_icon = QCheckBox("Icon/No icon")
        self.ch_icon.stateChanged.connect(self.view_icon_edit)

        self.file_path = PathEdit()
        self.file_path.setPlaceholderText("File Path")

        self.name = PathEdit()
        self.name.setPlaceholderText("Program name")

        self.icon_path = PathEdit()
        self.icon_path.setPlaceholderText("Icon Path")
        self.icon_path.hide()
        self.icon_path.setAcceptDrops(True)

        self.create_button = QPushButton('CREATE EXE')
        self.create_button.setCursor(Qt.PointingHandCursor)
        self.create_button.clicked.connect(self.create_exe)

        self.layout = QGridLayout()
        self.layout.addWidget(self.console, 0, 0, 1, 0)
        self.layout.addWidget(self.ch_console, 1, 1)
        self.layout.addWidget(self.ch_dir, 2, 1)
        self.layout.addWidget(self.ch_icon, 3, 1)
        self.layout.addWidget(self.file_path, 1, 2)
        self.layout.addWidget(self.name, 2, 2)
        self.layout.addWidget(self.icon_path, 3, 2)
        self.layout.addWidget(self.create_button, 4, 1, -1, -1)
        for raw in range(self.layout.rowCount()):
            self.layout.setRowMinimumHeight(raw, 100)
        self.layout.setSpacing(40)
        self.setLayout(self.layout)

        s = Style()
        self.setStyleSheet(s.style)

    def view_icon_edit(self):
        if self.ch_icon.isChecked():
            self.icon_path.show()
        else:
            self.icon_path.hide()

    def create_exe(self):
        try:
            cd = self.file_path.text().replace('/', '\\')
            cd = cd[1:] if cd[0] == '\\' else cd
            path = cd[:-(cd[::-1].index('\\')+1)]
            dist_path = ' --distpath "{}\\exe_program\\dist"'.format(path)
            work_path = ' --workpath "{}\\exe_program\\build"'.format(path)
            spec_path = ' --specpath "{}\\exe_program"'.format(path)
            cd = ' "{}"'.format(cd)

            icon_path = ''
            if self.ch_icon.isChecked():
                icon_path = self.icon_path.text().replace("/", "\\")
                icon_path = icon_path[1:] if icon_path[0] == '\\' else icon_path
            icon = '' if icon_path == '' else ' -i "{}"'.format(icon_path)

            dir_mode = ' -F' if self.ch_dir.isChecked() else ''

            console_mode = '' if self.ch_console.isChecked() else ' --noconsole'

            nameText = self.name.text()
            name = '' if nameText == '' else ' -n {}'.format(nameText)

            cmd = 'pyinstaller'+dist_path+work_path+spec_path+dir_mode+console_mode+name+icon+cd

            myproc = Popen(cmd, stdin=DEVNULL, stdout=PIPE, stderr=STDOUT)
            lines = myproc.stdout.readlines()
            text = '>>>  '+cmd+'\n' + \
                '\n'.join(list(map(lambda s: s.decode('utf-8'), lines)))

            self.console.setText(text)

        except Exception as err:
            self.console.setText(str(err))


if __name__ == "__main__":
    # app = QApplication([])
    app = QApplication()
    widget = MyWidget()

    import tkinter as tk

    root = tk.Tk()

    width = root.winfo_screenwidth() / 2
    height = root.winfo_screenheight() - 67
    del root

    widget.setMinimumWidth(width)
    widget.setMaximumWidth(width)
    widget.setMinimumHeight(height)
    widget.setMaximumHeight(height)
    del height
    widget.showMaximized()
    # widget.setMaximumWidth(width * 2)
    sys.exit(app.exec_())
