import sys
import random

import win32com.client

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from constructGUI import construct
from make_database import Multiplication

min_q = 11
max_q = 39

engine = create_engine('sqlite:///try_again.db')

class Window(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.speaker = win32com.client.Dispatch('SAPI.SpVoice')
        self.q1 = 0
        self.q2 = 0
        self.answer = 0
        self.playing = False
        self.session = sessionmaker(bind = engine)()
        
    def initUI(self):
        self.setWindowTitle("かけ算")

        self.num_label = construct(QLabel(), "settings.yaml", "label_1")

        self.setCentralWidget(self.num_label)

    def keyPressEvent(self, e):

        if e.key() == Qt.Key.Key_N:
            self.calc_exe()
        
        if e.key() == Qt.Key.Key_Q:
            self.close_Event()

        if e.key() == Qt.Key.Key_M:
            self.session.add(
                Multiplication(q1 = self.q1, q2 = self.q2)
            )
            self.session.commit()

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
    
    def close_Event(self):
        self.session.close()
        sys.exit()

if __name__ == "__main__":
    app = QApplication([])
    ex =Window()
    ex.show()
    app.exec()