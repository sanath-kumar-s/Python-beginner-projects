# ui/dashboard_view.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class DashboardView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("Spending Dashboard")
        title.setStyleSheet("font-size: 24px; color: white; margin-bottom: 10px;")
        self.layout.addWidget(title)

        # Charts Container
        self.charts_layout = QHBoxLayout()
        
        # Pie Chart
        self.pie_figure = Figure(figsize=(5, 5), facecolor='#1e1e1e')
        self.pie_canvas = FigureCanvas(self.pie_figure)
        self.charts_layout.addWidget(self.pie_canvas)
        
        # Bar Chart
        self.bar_figure = Figure(figsize=(5, 5), facecolor='#1e1e1e')
        self.bar_canvas = FigureCanvas(self.bar_figure)
        self.charts_layout.addWidget(self.bar_canvas)

        self.layout.addLayout(self.charts_layout)
        
        self.refresh_charts()

    def refresh_charts(self):
        self.update_pie_chart()
        self.update_bar_chart()

    def update_pie_chart(self):
        data = self.controller.get_category_distribution()
        self.pie_figure.clear()
        
        if not data:
            ax = self.pie_figure.add_subplot(111)
            ax.text(0.5, 0.5, "No Data Available", ha='center', va='center', color='white')
            ax.set_axis_off()
        else:
            categories = [row[0] for row in data]
            amounts = [row[1] for row in data]
            
            ax = self.pie_figure.add_subplot(111)
            wedges, texts, autotexts = ax.pie(amounts, labels=categories, autopct='%1.1f%%', 
                                             startangle=140, textprops={'color':"w"})
            ax.set_title("Expenses by Category", color='white', pad=20)
            
        self.pie_canvas.draw()

    def update_bar_chart(self):
        data = self.controller.get_spending_over_time()
        self.bar_figure.clear()
        
        if not data:
            ax = self.bar_figure.add_subplot(111)
            ax.text(0.5, 0.5, "No Data Available", ha='center', va='center', color='white')
            ax.set_axis_off()
        else:
            dates = [row[0] for row in data]
            amounts = [row[1] for row in data]
            
            # Show only last 7 entries for clarity if needed, or format dates
            ax = self.bar_figure.add_subplot(111)
            ax.bar(dates, amounts, color='#3d5afe')
            ax.set_title("Spending Over Time", color='white', pad=20)
            ax.tick_params(axis='x', rotation=45, colors='white')
            ax.tick_params(axis='y', colors='white')
            ax.set_facecolor('#1e1e1e')
            for spine in ax.spines.values():
                spine.set_color('#444')
            
        self.bar_figure.tight_layout()
        self.bar_canvas.draw()
