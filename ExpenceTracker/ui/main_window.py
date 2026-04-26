# ui/main_window.py
from PySide6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
                             QListWidget, QStackedWidget, QLabel, QFrame)
from PySide6.QtCore import Qt
from .add_expense_view import AddExpenseView
from .expense_table_view import ExpenseTableView
from .dashboard_view import DashboardView

class MainWindow(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Expense Tracker Pro")
        self.resize(1000, 700)
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(200)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 20, 0, 20)

        logo_label = QLabel("EXPENSE\nTRACKER")
        logo_label.setAlignment(Qt.AlignCenter)
        logo_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #3d5afe; padding: 20px;")
        sidebar_layout.addWidget(logo_label)

        self.nav_list = QListWidget()
        self.nav_list.setObjectName("sidebar_list")
        self.nav_list.addItem("Add Expense")
        self.nav_list.addItem("View Expenses")
        self.nav_list.addItem("Dashboard")
        self.nav_list.currentRowChanged.connect(self.switch_view)
        sidebar_layout.addWidget(self.nav_list)
        
        sidebar_layout.addStretch()
        main_layout.addWidget(sidebar)

        # Content Area
        self.stack = QStackedWidget()
        
        self.add_view = AddExpenseView(self.controller)
        self.table_view = ExpenseTableView(self.controller)
        self.dashboard_view = DashboardView(self.controller)
        
        self.stack.addWidget(self.add_view)
        self.stack.addWidget(self.table_view)
        self.stack.addWidget(self.dashboard_view)
        
        main_layout.addWidget(self.stack)

        # Connections
        self.add_view.expense_added.connect(self.table_view.load_data)
        self.add_view.expense_added.connect(self.dashboard_view.refresh_charts)
        self.table_view.data_changed.connect(self.dashboard_view.refresh_charts)

        self.nav_list.setCurrentRow(0)

    def switch_view(self, index):
        self.stack.setCurrentIndex(index)
        # Refresh views when switching
        if index == 1:
            self.table_view.load_data()
            self.table_view.refresh_filters()
        elif index == 2:
            self.dashboard_view.refresh_charts()
