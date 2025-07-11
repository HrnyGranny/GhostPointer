from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTextBrowser, QPushButton, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon
from src.gui.assets import get_icon

class HelpWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ghost Pointer - Help")
        self.setFixedSize(600, 500)
        app_icon = QIcon(get_icon('GhostPointer.ico'))
        self.setWindowIcon(app_icon)

        # Main layout
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Ghost Pointer - User Manual")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: #D0BCFF; margin-bottom: 10px;")
        
        # Help content
        self.help_content = QTextBrowser()
        self.help_content.setOpenExternalLinks(True)
        self.help_content.setStyleSheet("""
            background-color: #1A1A1A;
            border: 1px solid #31303A;
            border-radius: 8px;
            color: #E1E1E1;
            font-family: 'Segoe UI', 'Roboto', sans-serif;
            padding: 8px;
        """)
        
        # Set the help text
        self.help_content.setHtml(self.get_help_text())
        
        # Close button
        close_button = QPushButton("Close")
        close_button.setFixedWidth(120)
        close_button.clicked.connect(self.close)
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #6750A4;
                color: white;
                border-radius: 4px;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #7B68B5;
            }
            QPushButton:pressed {
                background-color: #553C9A;
            }
        """)
        
        # Add widgets to layout
        layout.addWidget(title)
        layout.addWidget(self.help_content)
        layout.addWidget(close_button, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Set dialog style
        self.setStyleSheet("""
            QDialog {
                background-color: #121212;
                color: #E1E1E1;
                font-family: 'Segoe UI', 'Roboto', sans-serif;
            }
        """)
    
    def get_help_text(self):
        return """
        <style>
            body { font-family: 'Segoe UI', 'Roboto', sans-serif; margin: 15px; color: #E1E1E1; }
            h2 { color: #D0BCFF; border-bottom: 1px solid #31303A; padding-bottom: 5px; }
            h3 { color: #E1E1E1; margin-top: 15px; }
            p { line-height: 1.5; }
            .key { background-color: #31303A; padding: 2px 5px; border-radius: 3px; font-family: 'Consolas', 'Courier New', monospace; color: #D0BCFF; }
            .section { margin-bottom: 20px; }
            .tip { background-color: #1E1E1E; padding: 10px; border-left: 4px solid #6750A4; margin: 10px 0; }
            ul { color: #E1E1E1; }
            a { color: #D0BCFF; }
        </style>
        
        <div class="section">
            <h2>What is Ghost Pointer?</h2>
            <p>Ghost Pointer is an application that allows you to automate mouse movements and clicks to prevent your computer from entering idle mode or to maintain your "Active" status on messaging platforms.</p>
        </div>
        
        <div class="section">
            <h2>Main Tabs</h2>
            
            <h3>Random Movement</h3>
            <p>Moves the mouse cursor randomly within a specified area to simulate activity.</p>
            <ul>
                <li>Click the button to start/stop random movement.</li>
                <li>The counter shows how long the movement has been active.</li>
            </ul>
            
            <h3>Auto Click</h3>
            <p>Performs automatic clicks at specific or random positions.</p>
            <ul>
                <li>Click the button to start/stop automatic clicks.</li>
                <li>The counter shows how long the auto-click has been active.</li>
            </ul>
        </div>
        
        <div class="section">
            <h2>Developer Mode</h2>
            <p>Activate developer mode using the switch in the upper right corner. This will display the console with detailed information about what the application is doing.</p>
        </div>
        
        <div class="section">
            <h2>Keyboard Shortcuts</h2>
            <ul>
                <li><span class="key">Ctrl+Space</span> - Start/stop the current action</li>
                <li><span class="key">ESC</span> - Stop any ongoing operation</li>
            </ul>
        </div>
        
        <div class="tip">
            <strong>Tip:</strong> To avoid issues with security-sensitive applications, disable Ghost Pointer before using banking or corporate applications.
        </div>
        
        <p style="text-align: center; margin-top: 20px; color: #8F8F8F;">
            Ghost Pointer v1.2.0 — Developed by @HrnyGranny
        </p>
        """