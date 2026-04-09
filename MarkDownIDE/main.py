import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QFileDialog, QTextEdit, QTreeView,
    QSplitter
)
from PyQt6.QtGui import QFileSystemModel
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QDragEnterEvent, QDropEvent
from PyQt6.QtCore import QUrl

import markdown


class MarkdownIDE(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Markdown IDE")
        self.resize(1400, 900)
        self.setAcceptDrops(True)

        self.current_file = None

        # Layout
        main_widget = QWidget()
        main_layout = QHBoxLayout()

        # Sidebar (File Explorer)
        self.model = QFileSystemModel()
        self.model.setRootPath(os.getcwd())

        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(os.getcwd()))
        self.tree.clicked.connect(self.open_from_sidebar)

        # Editor
        self.editor = QTextEdit()
        self.editor.textChanged.connect(self.update_preview)

        # Preview (browser)
        self.preview = QWebEngineView()

        # Splitter (editor + preview)
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self.editor)
        splitter.addWidget(self.preview)
        splitter.setSizes([600, 800])

        # Top buttons
        top_bar = QHBoxLayout()

        open_btn = QPushButton("Open")
        open_btn.clicked.connect(self.open_file)

        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save_file)

        export_btn = QPushButton("Export PDF")
        export_btn.clicked.connect(self.export_pdf)

        top_bar.addWidget(open_btn)
        top_bar.addWidget(save_btn)
        top_bar.addWidget(export_btn)

        # Center layout
        center_layout = QVBoxLayout()
        center_layout.addLayout(top_bar)
        center_layout.addWidget(splitter)

        main_layout.addWidget(self.tree, 2)
        main_layout.addLayout(center_layout, 5)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        self.load_css()

    # ---------------- CSS ----------------
    def load_css(self):
        try:
            with open("assets/github-dark.css", "r") as f:
                self.github_css = f.read()
        except:
            self.github_css = ""

        try:
            with open("assets/highlight.css", "r") as f:
                self.highlight_css = f.read()
        except:
            self.highlight_css = ""

    # ---------------- File Handling ----------------
    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open File", "", "Markdown Files (*.md)"
        )
        if file_path:
            self.load_file(file_path)

    def open_from_sidebar(self, index):
        path = self.model.filePath(index)
        if path.endswith(".md"):
            self.load_file(path)

    def load_file(self, path):
        with open(path, "r", encoding="utf-8") as f:
            self.editor.setText(f.read())
        self.current_file = path
        self.update_preview()

    def save_file(self):
        if not self.current_file:
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Save File", "", "Markdown Files (*.md)"
            )
            if not file_path:
                return
            self.current_file = file_path

        with open(self.current_file, "w", encoding="utf-8") as f:
            f.write(self.editor.toPlainText())

    # ---------------- Preview ----------------
    def update_preview(self):
        md_text = self.editor.toPlainText()

        md_text = self.parse_alerts(md_text)

        html = markdown.markdown(
            md_text,
            extensions=["fenced_code", "tables", "codehilite"]
        )

        base_dir = os.path.dirname(self.current_file) if self.current_file else os.getcwd()

        full_html = f"""
        <html>
        <head>
        <style>
        {self.github_css}
        {self.highlight_css}

        body {{
            background-color: #0d1117;
            color: #c9d1d9;
        }}

        img {{
            max-width: 100%;
            border-radius: 8px;
            margin: 10px 0;
        }}

        .markdown-body {{
            max-width: 900px;
            margin: auto;
            padding: 40px;
            line-height: 1.7;
            font-size: 16px;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI",
                        "Noto Color Emoji", "Apple Color Emoji", sans-serif;
        }}

        /* Improve headings */
        h1, h2, h3 {{
            border-bottom: 1px solid #30363d;
            padding-bottom: 6px;
        }}

        /* Better blockquotes */
        blockquote {{
            border-left: 4px solid #3b82f6;
            padding: 10px 16px;
            margin: 16px 0;
            background-color: #161b22;
            color: #8b949e;
            border-radius: 6px;
        }}

        /* Alert boxes */
        .alert {{
            padding: 12px 16px;
            margin: 16px 0;
            border-radius: 8px;
            font-weight: 500;
        }}

        .alert-note {{
            background-color: #1f6feb20;
            border-left: 4px solid #1f6feb;
        }}

        .alert-warning {{
            background-color: #d2992220;
            border-left: 4px solid #d29922;
        }}

        .alert-danger {{
            background-color: #f8514920;
            border-left: 4px solid #f85149;
        }}

        .alert-tip {{
            background-color: #23863620;
            border-left: 4px solid #238636;
        }}

        /* Code blocks */
        pre {{
            background-color: #161b22;
            padding: 16px;
            border-radius: 10px;
            overflow-x: auto;
        }}

        code {{
            background-color: #161b22;
            padding: 3px 6px;
            border-radius: 6px;
        }}

        /* Links */
        a {{
            color: #58a6ff;
        }}

        </style>
        </head>

        <body>
        <article class="markdown-body">
        {html}
        </article>
        </body>
        </html>
        """

        
        self.preview.setHtml(
            full_html,
            QUrl.fromLocalFile(base_dir + "/")
        )

    def parse_alerts(self, text):
        lines = text.split("\n")
        result = []

        for line in lines:
            stripped = line.strip()

            if stripped.startswith(">[!NOTE]"):
                content = stripped.replace(">[!NOTE]", "").strip()
                result.append(f'<div class="alert alert-note">📝 {content}</div>')

            elif stripped.startswith(">[!WARNING]"):
                content = stripped.replace(">[!WARNING]", "").strip()
                result.append(f'<div class="alert alert-warning">⚠️ {content}</div>')

            elif stripped.startswith(">[!TIP]"):
                content = stripped.replace(">[!TIP]", "").strip()
                result.append(f'<div class="alert alert-tip">💡 {content}</div>')

            elif stripped.startswith(">[!DANGER]"):
                content = stripped.replace(">[!DANGER]", "").strip()
                result.append(f'<div class="alert alert-danger">🚨 {content}</div>')

            else:
                result.append(line)

        return "\n".join(result)

    # ---------------- Drag & Drop ----------------
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if file_path.endswith(".md"):
                self.load_file(file_path)

    # ---------------- Export PDF ----------------
    def export_pdf(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export PDF", "", "PDF Files (*.pdf)"
        )
        if not file_path:
            return

        def callback(*args):
            print("PDF saved")

        self.preview.page().printToPdf(file_path)


# ---------------- RUN ----------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MarkdownIDE()
    window.show()
    sys.exit(app.exec())