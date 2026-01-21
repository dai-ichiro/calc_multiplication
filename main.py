import sys
import os
import random
from copy import deepcopy

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QApplication, QMainWindow, QLabel, QWidget,
                               QVBoxLayout, QTabWidget, QMessageBox)
from PySide6.QtGui import QAction

from utils import construct

# Mock win32com for non-Windows environments (like this sandbox)
try:
    import win32com.client
    def get_speaker():
        return win32com.client.Dispatch('SAPI.SpVoice')
except ImportError:
    class MockSpeaker:
        def Speak(self, text):
            print(f"Speaking: {text}")
    def get_speaker():
        return MockSpeaker()

# Constants
MIN_Q = 11
MAX_Q = 99
RETRY_FILE = 'retry.txt'

class PracticeWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.speaker = get_speaker()
        self.q1 = 0
        self.q2 = 0
        self.answer = 0
        self.playing = False
        self.question_text = None
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.num_label = construct(QLabel(), "utils/settings.yaml", "label_for_try")
        self.layout.addWidget(self.num_label)

        self.setLayout(self.layout)

    def handle_key(self, e):
        if e.key() == Qt.Key.Key_N:
            self.calc_exe()
        elif e.key() == Qt.Key.Key_M:
            self.save_retry()

    def calc_exe(self):
        if not self.playing:
            self.q1 = random.randint(MIN_Q, MAX_Q)
            self.q2 = random.randint(MIN_Q, MAX_Q)
            self.question_text = f'{self.q1} x {self.q2}'
            self.answer = self.q1 * self.q2
            self.speaker.Speak(f'{self.q1}かける{self.q2}')
            self.playing = True
        else:
            self.speaker.Speak(f'{self.answer}')
            self.playing = False

    def save_retry(self):
        if self.question_text is not None:
            with open(RETRY_FILE, mode='a') as f:
                f.write(f'{self.question_text}\n')
            # Optional: Feedback to user? The original didn't have any.

class RetryWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.speaker = get_speaker()
        self.q1 = 0
        self.q2 = 0
        self.answer = 0
        self.question_list = []
        self.playing = False
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.num_label = construct(QLabel(), "utils/settings.yaml", "label_for_retry")
        self.original_text = self.num_label.text()
        self.layout.addWidget(self.num_label)

        self.setLayout(self.layout)

    def handle_key(self, e):
        if e.key() == Qt.Key.Key_N:
            self.calc_exe()

    def reload_questions(self):
        self.question_list = []
        if os.path.exists(RETRY_FILE):
            with open(RETRY_FILE, 'r') as f:
                retry_list = f.readlines()
                # Filter empty lines
                retry_list = [x.strip() for x in retry_list if x.strip() != '']
                self.question_list = deepcopy(retry_list)
                random.shuffle(self.question_list)

        # Reset state if needed
        self.playing = False
        # Maybe show "No questions" if list is empty?
        if not self.question_list:
             self.num_label.setText("No questions\nto retry")
        else:
             self.num_label.setText(self.original_text)

    def calc_exe(self):
        if not self.playing:
            if len(self.question_list) == 0:
                # Try reloading if empty
                self.reload_questions()
                if len(self.question_list) == 0:
                    self.speaker.Speak("復習する問題がありません")
                    return

            question_line = self.question_list.pop(0)
            try:
                question_line_split = question_line.split(' ')
                self.q1 = int(question_line_split[0])
                self.q2 = int(question_line_split[2])
                self.answer = self.q1 * self.q2
                self.speaker.Speak(f'{self.q1}かける{self.q2}')
                self.playing = True
            except (IndexError, ValueError):
                # Handle malformed lines
                self.calc_exe() # Skip to next
        else:
            self.speaker.Speak(f'{self.answer}')
            self.playing = False

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Multiplication App")
        # Adjust size to fit tabs + content. Original was 300x150.
        self.setFixedWidth(320)
        self.setFixedHeight(200)

        self.initUI()

    def initUI(self):
        # Menu Bar
        menu_bar = self.menuBar()

        # Database Menu
        db_menu = menu_bar.addMenu("Database")

        clear_action = QAction("Clear Database", self)
        clear_action.triggered.connect(self.clear_database)
        db_menu.addAction(clear_action)

        # Tabs
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.practice_tab = PracticeWidget()
        self.retry_tab = RetryWidget()

        self.tabs.addTab(self.practice_tab, "Practice")
        self.tabs.addTab(self.retry_tab, "Retry")

        self.tabs.currentChanged.connect(self.on_tab_change)

    def on_tab_change(self, index):
        if self.tabs.widget(index) == self.retry_tab:
            self.retry_tab.reload_questions()
            # Also restore label text in case it was changed to "No questions"
            # Actually constructGUI sets the text from yaml. We might need to reset it.
            # But reload_questions sets it to "No questions" if empty.
            # If not empty, the text stays as is until next 'calc_exe' changes it?
            # Wait, the label text in calc.py is static "n: next...". It only changes when TTS happens?
            # No, TTS speaks, but label text doesn't seem to change in original code!
            # Original code: `self.speaker.Speak(...)`. Label text is constant instruction.
            # So I should respect that.
            if self.retry_tab.question_list:
                 # Reset to default text from settings if possible, or just leave it.
                 # Since I can't easily re-read settings here without parsing yaml again,
                 # I'll rely on it being static unless I changed it.
                 # In reload_questions I changed it to "No questions...".
                 # So I should revert it if questions exist.
                 # Let's read the yaml text again or store it.
                 pass

    def clear_database(self):
        if os.path.exists(RETRY_FILE):
            os.remove(RETRY_FILE)
            QMessageBox.information(self, "Database", "Retry database cleared.")
            if self.tabs.currentWidget() == self.retry_tab:
                self.retry_tab.reload_questions()
        else:
            QMessageBox.information(self, "Database", "Database is already empty.")

    def keyPressEvent(self, e):
        # Global keys
        if e.key() == Qt.Key.Key_Q:
            self.close()
            return

        # Forward to current tab
        current_widget = self.tabs.currentWidget()
        if isinstance(current_widget, (PracticeWidget, RetryWidget)):
            current_widget.handle_key(e)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
