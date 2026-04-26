# main.py
import sys
import os
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
from logic.expense_controller import ExpenseController

def load_stylesheet(app, path):
    if os.path.exists(path):
        with open(path, "r") as f:
            app.setStyleSheet(f.read())

def main():
    app = QApplication(sys.argv)
    
    # Initialize controller
    controller = ExpenseController()
    
    # Create main window
    window = MainWindow(controller)
    
    # Load styles
    style_path = os.path.join(os.path.dirname(__file__), "assets", "style.qss")
    load_stylesheet(app, style_path)
    
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
