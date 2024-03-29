import random
import win32com.client
from copy import deepcopy

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QApplication, QLabel

from constructGUI import construct

#question_list
import os
assert os.path.exists('retry.txt'), 'file not exits'

with open('retry.txt', 'r') as f:
    retry_list = f.readlines()
    retry_list = [x.strip() for x in retry_list if x.strip() != '']

class Window(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.speaker = win32com.client.Dispatch('SAPI.SpVoice')
        self.q1 = 0
        self.q2 = 0
        self.answer = 0
        self.question_list = []
        self.playing = False
        
    def initUI(self):
        self.setWindowTitle("multiplication")
        self.setFixedWidth(300)
        self.setFixedHeight(150)

        self.num_label = construct(QLabel(), "settings.yaml", "label_for_retry")

        self.setCentralWidget(self.num_label)

    def keyPressEvent(self, e):

        if e.key() == Qt.Key.Key_N:
            self.calc_exe()
        
        if e.key() == Qt.Key.Key_Q:
            self.close_Event()

    def calc_exe(self):
        if self.playing == False:
            if len(self.question_list) == 0:
                self.question_list = deepcopy(retry_list)
                random.shuffle(self.question_list)
            question_line = self.question_list.pop(0)
            question_line_split = question_line.split(' ')
            self.q1 = int(question_line_split[0])
            self.q2 = int(question_line_split[2])
            self.answer = self.q1 * self.q2
            self.speaker.Speak(f'{self.q1}かける{self.q2}')
            self.playing = not self.playing
        else:
            self.speaker.Speak('%d'%self.answer)
            self.playing = not self.playing
    
    def close_Event(self):
        self.close()

if __name__ == "__main__":
    app = QApplication([])
    ex =Window()
    ex.show()
    app.exec()
