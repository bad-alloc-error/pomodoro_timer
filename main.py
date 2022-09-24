from PyQt5.QtWidgets import QApplication
from pomodoro import Pomodoro
from style_sheet import style_sheet
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(style_sheet)
    window = Pomodoro()
    sys.exit(app.exec_())