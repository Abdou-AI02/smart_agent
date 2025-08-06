import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLineEdit, QPushButton, QTextEdit, 
                             QSplitter, QListWidget, QListWidgetItem, QSizePolicy)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QIcon
import threading
import time

# assuming the directory structure is set up correctly
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from agents.main_agent import MainAgent
from modules.notifier import Notifier
from config import APP_TITLE_AR

# Worker thread to process agent commands without freezing the UI
class AgentWorker(QThread):
    response_ready = pyqtSignal(str)
    logs_ready = pyqtSignal(str)
    memory_cleared = pyqtSignal()

    def __init__(self, agent):
        super().__init__()
        self.agent = agent
        self.user_input = ""
        self.is_clear_memory_command = False

    def run(self):
        if self.is_clear_memory_command:
            self.agent.memory_manager.clear_memory()
            self.memory_cleared.emit()
            return
            
        response = self.agent.process_command(self.user_input)
        logs = self.agent.get_logs()
        self.agent.clear_logs()
        self.response_ready.emit(response)
        self.logs_ready.emit(logs)

class ChatWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.agent = MainAgent()
        self.notifier = Notifier()
        self.setWindowTitle(APP_TITLE_AR)
        self.setWindowIcon(QIcon('path/to/your/icon.png')) # Replace with your icon path
        self.setGeometry(100, 100, 1200, 800)

        # Main layout
        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        self.setCentralWidget(main_splitter)

        # Left side: Chat UI
        chat_widget = QWidget()
        chat_layout = QVBoxLayout(chat_widget)
        
        self.chat_history = QListWidget()
        self.chat_history.setAlternatingRowColors(True)
        self.chat_history.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        chat_layout.addWidget(self.chat_history)

        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("اكتب رسالتك هنا... / Type your message here...")
        self.input_box.setFont(QFont("Arial", 12))
        self.input_box.returnPressed.connect(self.send_message)
        chat_layout.addWidget(self.input_box)

        # Buttons
        button_layout = QHBoxLayout()
        send_btn = QPushButton("إرسال / Send")
        send_btn.clicked.connect(self.send_message)
        clear_btn = QPushButton("مسح الذاكرة / Clear Memory")
        clear_btn.clicked.connect(self.clear_memory)
        button_layout.addWidget(send_btn)
        button_layout.addWidget(clear_btn)
        chat_layout.addLayout(button_layout)
        
        main_splitter.addWidget(chat_widget)

        # Right side: Logs and Help
        right_splitter = QSplitter(Qt.Orientation.Vertical)
        
        self.logs_output = QTextEdit()
        self.logs_output.setReadOnly(True)
        self.logs_output.setPlaceholderText("سجلات الوكيل / Agent Logs...")
        self.logs_output.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        right_splitter.addWidget(self.logs_output)

        self.help_output = QTextEdit()
        self.help_output.setReadOnly(True)
        self.help_output.setMarkdown(self.agent.get_help())
        self.help_output.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        right_splitter.addWidget(self.help_output)
        
        main_splitter.addWidget(right_splitter)

        # Set initial sizes for the splitters
        main_splitter.setSizes([800, 400])
        right_splitter.setSizes([400, 400])

        self.worker = AgentWorker(self.agent)
        self.worker.response_ready.connect(self.display_response)
        self.worker.logs_ready.connect(self.display_logs)
        self.worker.memory_cleared.connect(self.on_memory_cleared)

        self.thread = threading.Thread(target=self.check_for_notifications)
        self.thread.daemon = True
        self.thread.start()

    def send_message(self):
        user_input = self.input_box.text()
        if not user_input.strip():
            return
        
        self.add_chat_item(f"أنت: {user_input}", "user")
        self.input_box.clear()
        
        self.worker.user_input = user_input
        self.worker.is_clear_memory_command = False
        self.worker.start()

    def display_response(self, response):
        self.add_chat_item(f"الوكيل: {response}", "agent")
        self.notifier.send_notification("تمت المهمة!", "الوكيل لديه رد جديد.")

    def display_logs(self, logs):
        self.logs_output.setText(logs)

    def clear_memory(self):
        self.worker.is_clear_memory_command = True
        self.worker.start()

    def on_memory_cleared(self):
        self.chat_history.clear()
        self.add_chat_item("تم مسح ذاكرة المحادثة.", "system")

    def add_chat_item(self, text, role):
        item = QListWidgetItem(text)
        if role == "user":
            item.setForeground(Qt.GlobalColor.darkBlue)
            item.setTextAlignment(Qt.AlignmentFlag.AlignRight)
        elif role == "agent":
            item.setForeground(Qt.GlobalColor.darkGreen)
            item.setTextAlignment(Qt.AlignmentFlag.AlignLeft)
        elif role == "system":
            item.setForeground(Qt.GlobalColor.darkGray)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.chat_history.addItem(item)
        self.chat_history.scrollToBottom()

    def check_for_notifications(self):
        # A placeholder for future, more complex notification logic
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ChatWindow()
    window.show()
    sys.exit(app.exec())