import random
import win32com.client

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QApplication, QLabel

from constructGUI import construct

min_q = 11
max_q = 99

class Window(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.speaker = win32com.client.Dispatch('SAPI.SpVoice')
        self.q1 = 0
        self.q2 = 0
        self.answer = 0
        self.playing = False
        self.question_text = None
        
    def initUI(self):
        
        self.setWindowTitle("multiplication")
        self.setFixedWidth(300)
        self.setFixedHeight(150)

        self.num_label = construct(QLabel(), "settings.yaml", "label_1")

        self.setCentralWidget(self.num_label)

    def keyPressEvent(self, e):

        if e.key() == Qt.Key_N:
            self.calc_exe()
        
        if e.key() == Qt.Key_Q:
            self.close_Event()

        if e.key() == Qt.Key_M:
            if self.question_text is not None:
                with open('retry.txt', mode='a') as f:
                    f.write(f'{self.question_text}\n')

    def calc_exe(self):
        if self.playing == False:
            self.q1 = random.randint(min_q,max_q)
            self.q2 = random.randint(min_q,max_q)
            self.question_text = f'{self.q1} x {self.q2}'
            self.answer = self.q1 * self.q2
            self.speaker.Speak(f'{self.q1}かける{self.q2}')
            self.playing = not self.playing
        else:
            self.speaker.Speak(f'{self.answer}')
            self.playing = not self.playing
    
    def close_Event(self):
        self.close()

if __name__ == "__main__":
    app = QApplication([])
    ex =Window()
    ex.show()
    app.exec()