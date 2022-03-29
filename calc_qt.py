
import sys
import win32com.client
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QFont
import random

min_q = 11
max_q = 22

class Window(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.speaker = win32com.client.Dispatch('SAPI.SpVoice')
        self.q1 = 0
        self.q2 = 0
        self.answer = 0
        self.playing = False
        
    def initUI(self):
        self.setWindowTitle("かけ算")

        font = QFont()
        font.setFamily('Times')
        font.setPointSize(20)
        font.setBold(True)

        self.num_label = QLabel()
        self.num_label.setFixedSize(QSize(300,100))
        self.num_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFont(font)
        self.num_label.setText('start')

        layout = QVBoxLayout()
        layout.addWidget(self.num_label)
        self.setLayout(layout)

    def keyPressEvent(self, e):

        if e.key() == Qt.Key.Key_N:
            self.calc_exe()
        
        if e.key() == Qt.Key.Key_Q:
            sys.exit()

    def calc_exe(self):
        if self.playing == False:
            self.q1 = random.randint(min_q,max_q)
            self.q2 = random.randint(min_q,max_q)
            self.num_label.setText('%d x %d'%(self.q1, self.q2))
            self.answer = self.q1 * self.q2
            self.speaker.Speak('%dかける%d'%(self.q1, self.q2))
            self.playing = not self.playing
        else:
            self.speaker.Speak('%d'%self.answer)
            self.playing = not self.playing

if __name__ == "__main__":
    app = QApplication([])
    ex =Window()
    ex.show()
    app.exec()