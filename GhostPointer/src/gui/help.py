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
            h4 { color: #D0BCFF; margin-top: 12px; margin-bottom: 8px; }
            p { line-height: 1.5; }
            .key { background-color: #31303A; padding: 2px 5px; border-radius: 3px; font-family: 'Consolas', 'Courier New', monospace; color: #D0BCFF; }
            .section { margin-bottom: 20px; }
            .tip { background-color: #1E1E1E; padding: 10px; border-left: 4px solid #6750A4; margin: 10px 0; }
            .note { background-color: #1E1E1E; padding: 10px; border-left: 4px solid #FFB4A1; margin: 10px 0; }
            ul { color: #E1E1E1; }
            li { margin-bottom: 5px; }
            a { color: #D0BCFF; }
            .feature { color: #D0BCFF; font-weight: bold; }
            .control { border-bottom: 1px dotted #6750A4; }
        </style>
        
        <div class="section">
            <h2>What is Ghost Pointer?</h2>
            <p>Ghost Pointer is an application that allows you to automate mouse movements and clicks to prevent your computer from entering idle mode or to maintain your "Active" status on messaging platforms.</p>
        </div>
        
        <div class="section">
            <h2>Getting Started</h2>
            <p>To start or stop any action, you can either:</p>
            <ul>
                <li>Click the large <span class="feature">Play/Stop button</span> in the center of the application</li>
                <li>Use the keyboard shortcut <span class="key">Ctrl+Space</span></li>
            </ul>
            <p>The timer at the bottom of the window shows how long the current action has been running.</p>
        </div>
        
        <div class="section">
            <h2>Movement Tab</h2>
            <p>This tab allows you to configure how the mouse cursor moves automatically across your screen.</p>
            
            <h4>Movement Area</h4>
            <ul>
                <li><span class="feature">Fullscreen</span>: Mouse moves across your entire screen</li>
                <li><span class="feature">Sized</span>: Select a specific area for mouse movement by drawing a rectangle on your screen</li>
            </ul>
            
            <h4>Movement Settings</h4>
            <ul>
                <li><span class="control">Speed</span>: Controls how fast the mouse cursor moves (1-10)</li>
                <li><span class="control">Delay</span>: Time between each movement in milliseconds</li>
                <li><span class="control">Stop on manual move</span>: When enabled, Ghost Pointer will stop automatic movement if you move the mouse manually</li>
            </ul>
            
            <div class="note">
                <strong>Note:</strong> When using "Sized" mode, you'll be prompted to select an area on your screen before the movement begins.
            </div>
        </div>
        
        <div class="section">
            <h2>Click Tab</h2>
            <p>This tab allows you to configure automatic mouse clicks.</p>
            
            <h4>Click Type</h4>
            <ul>
                <li><span class="feature">Left Click</span>: Simulates left mouse button clicks</li>
                <li><span class="feature">Right Click</span>: Simulates right mouse button clicks</li>
            </ul>
            
            <h4>Click Position</h4>
            <ul>
                <li><span class="feature">Current</span>: Clicks at wherever the mouse cursor currently is</li>
                <li><span class="feature">Select</span>: Prompts you to select a specific position where all clicks will occur</li>
            </ul>
            
            <h4>Click Settings</h4>
            <ul>
                <li><span class="control">Interval</span>: Time between clicks in seconds</li>
                <li><span class="control">Jitter</span>: When enabled, adds a tiny 1-pixel movement to each click to simulate human activity</li>
                <li><span class="control">Limit</span>: You can set limits for auto-clicking:
                    <ul>
                        <li><span class="feature">Infinite</span>: Clicks continue until manually stopped</li>
                        <li><span class="feature">Time</span>: Click for a specific duration in seconds</li>
                        <li><span class="feature">Clicks</span>: Perform a specific number of clicks</li>
                    </ul>
                </li>
            </ul>
        </div>
        
        <div class="section">
            <h2>Developer Mode</h2>
            <p>Activate developer mode using the switch in the upper right corner. This will display a console with detailed information about what the application is doing, including:</p>
            <ul>
                <li>Action start/stop events</li>
                <li>Configuration details</li>
                <li>Error messages</li>
            </ul>
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
            Ghost Pointer v1.0.0 — Developed by @HrnyGranny
        </p>
        """