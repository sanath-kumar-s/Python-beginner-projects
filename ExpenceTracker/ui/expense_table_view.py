# ui/expense_table_view.py
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
                             QTableWidgetItem, QPushButton, QComboBox, 
                             QLabel, QDateEdit, QHeaderView, QMessageBox)
from PySide6.QtCore import Qt, QDate, Signal

class ExpenseTableView(QWidget):
    data_changed = Signal()

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Filters Row
        filter_layout = QHBoxLayout()
        
        filter_layout.addWidget(QLabel("Category:"))
        self.category_filter = QComboBox()
        self.category_filter.currentIndexChanged.connect(self.load_data)
        filter_layout.addWidget(self.category_filter)

        filter_layout.addWidget(QLabel("From:"))
        self.from_date = QDateEdit()
        self.from_date.setCalendarPopup(True)
        self.from_date.setDate(QDate.currentDate().addMonths(-1))
        self.from_date.dateChanged.connect(self.load_data)
        filter_layout.addWidget(self.from_date)

        filter_layout.addWidget(QLabel("To:"))
        self.to_date = QDateEdit()
        self.to_date.setCalendarPopup(True)
        self.to_date.setDate(QDate.currentDate())
        self.to_date.dateChanged.connect(self.load_data)
        filter_layout.addWidget(self.to_date)

        filter_layout.addStretch()
        
        self.delete_btn = QPushButton("Delete Selected")
        self.delete_btn.setObjectName("delete_btn")
        self.delete_btn.clicked.connect(self.delete_selected)
        filter_layout.addWidget(self.delete_btn)

        layout.addLayout(filter_layout)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Date", "Category", "Amount ($)", "Note"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSortingEnabled(True)
        
        layout.addWidget(self.table)

        self.refresh_filters()
        self.load_data()

    def refresh_filters(self):
        self.category_filter.blockSignals(True)
        self.category_filter.clear()
        self.category_filter.addItem("All")
        categories = self.controller.get_categories()
        self.category_filter.addItems(categories)
        self.category_filter.blockSignals(False)

    def load_data(self):
        category = self.category_filter.currentText()
        start = self.from_date.date().toString("yyyy-MM-dd")
        end = self.to_date.date().toString("yyyy-MM-dd")
        
        expenses = self.controller.get_expenses(start, end, category)
        
        self.table.setSortingEnabled(False)
        self.table.setRowCount(0)
        for row_idx, row_data in enumerate(expenses):
            self.table.insertRow(row_idx)
            for col_idx, item in enumerate(row_data):
                cell = QTableWidgetItem(str(item))
                if col_idx == 3: # Amount column
                    cell.setData(Qt.DisplayRole, float(item))
                self.table.setItem(row_idx, col_idx, cell)
        
        self.table.setSortingEnabled(True)
        # Hide ID column
        self.table.setColumnHidden(0, True)

    def delete_selected(self):
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Selection Error", "Please select an expense to delete.")
            return

        reply = QMessageBox.question(self, "Confirm Delete", 
                                   "Are you sure you want to delete the selected expense(s)?",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            for row in selected_rows:
                expense_id = int(self.table.item(row.row(), 0).text())
                self.controller.delete_expense(expense_id)
            
            self.load_data()
            self.data_changed.emit()
