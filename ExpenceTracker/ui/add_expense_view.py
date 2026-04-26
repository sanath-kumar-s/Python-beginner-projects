# ui/add_expense_view.py
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QLineEdit, 
                             QComboBox, QDateEdit, QTextEdit, QPushButton, 
                             QLabel, QMessageBox)
from PySide6.QtCore import QDate, Signal

class AddExpenseView(QWidget):
    expense_added = Signal()

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        title = QLabel("Add New Expense")
        title.setStyleSheet("font-size: 24px; color: white; margin-bottom: 20px;")
        layout.addWidget(title)

        form_layout = QFormLayout()
        form_layout.setSpacing(15)

        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("0.00")
        
        self.category_input = QComboBox()
        self.refresh_categories()

        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate())

        self.note_input = QTextEdit()
        self.note_input.setMaximumHeight(100)
        self.note_input.setPlaceholderText("Optional notes...")

        form_layout.addRow("Amount ($)", self.amount_input)
        form_layout.addRow("Category", self.category_input)
        form_layout.addRow("Date", self.date_input)
        form_layout.addRow("Note", self.note_input)

        layout.addLayout(form_layout)

        self.submit_btn = QPushButton("Save Expense")
        self.submit_btn.clicked.connect(self.save_expense)
        layout.addWidget(self.submit_btn)
        
        layout.addStretch()

    def refresh_categories(self):
        self.category_input.clear()
        categories = self.controller.get_categories()
        self.category_input.addItems(categories)

    def save_expense(self):
        try:
            amount_str = self.amount_input.text()
            if not amount_str:
                raise ValueError("Amount is required")
            
            amount = float(amount_str)
            category = self.category_input.currentText()
            date = self.date_input.date().toString("yyyy-MM-dd")
            note = self.note_input.toPlainText()

            self.controller.add_expense(amount, category, date, note)
            
            QMessageBox.information(self, "Success", "Expense added successfully!")
            self.clear_form()
            self.expense_added.emit()
            
        except ValueError as e:
            QMessageBox.warning(self, "Input Error", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {str(e)}")

    def clear_form(self):
        self.amount_input.clear()
        self.date_input.setDate(QDate.currentDate())
        self.note_input.clear()
        if self.category_input.count() > 0:
            self.category_input.setCurrentIndex(0)
