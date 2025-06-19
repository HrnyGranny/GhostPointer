def get_app_styles():
    return """
        QWidget {
            background-color: #121212;
            color: #E1E1E1;
            font-family: 'Segoe UI', 'Roboto', sans-serif;
            font-size: 12px;
        }
        
        QPushButton#optionButton {
            background-color: #1E1E1E;
            color: #E1E1E1;
            border: 1px solid #31303A;
            border-radius: 6px;
            padding: 8px 12px;
            font-weight: 500;
            min-height: 32px;
        }
        
        QPushButton#optionButton:hover {
            background-color: #2A2A2A;
            border: 1px solid #6750A4;
        }
        
        QPushButton#optionButton:checked {
            background-color: #31303A;
            border: 1px solid #6750A4;
            color: #D0BCFF;
        }
        
        QSlider::groove:horizontal {
            border: none;
            height: 4px;
            background: #31303A;
            margin: 0;
            border-radius: 2px;
        }
        
        QSlider::handle:horizontal {
            background: #6750A4;
            border: none;
            width: 16px;
            height: 16px;
            margin: -6px 0;
            border-radius: 8px;
        }
        
        QSlider::handle:horizontal:hover {
            background: #7965B5;
            width: 18px;
            height: 18px;
            margin: -7px 0;
            border-radius: 9px;
        }
        
        QFrame#optionsFrameWithBg {
            border: 1px solid #31303A;
            border-radius: 10px;
            background-color: #1A1A1A;
        }
        
        QFrame#transparentFrame {
            border: none;
            background-color: transparent;
        }
        
        QCheckBox {
            spacing: 6px;
            min-height: 26px;
            padding-left: 4px;
        }
        
        QCheckBox::indicator {
            width: 18px;
            height: 18px;
        }
        
        QCheckBox::indicator::unchecked {
            border: 2px solid #7A7289;
            background: transparent;
            border-radius: 4px;
        }
        
        QCheckBox::indicator::checked {
            border: 2px solid #6750A4;
            background: #6750A4;
            border-radius: 4px;
        }
        
        QCheckBox:hover {
            color: #D0BCFF;
            background-color: rgba(208, 188, 255, 0.08);
            border-radius: 6px;
        }
        
        QLabel#shortcutLabel {
            color: #8F8F8F;
            font-size: 11px;
            font-style: italic;
            font-weight: 400;
            margin-top: 4px;
        }
        
        #consoleOutput {
            background-color: #1A1A1A;
            border: 1px solid #31303A;
            border-radius: 8px;
            color: #E1E1E1;
            font-family: 'Consolas', 'Courier New', monospace;
            font-size: 11px;
            padding: 8px;
        }
        
        QSpinBox {
            background-color: #2A2A2A;
            border: 1px solid #31303A;
            border-radius: 4px;
            padding: 2px 8px;
            color: #E1E1E1;
        }
        
        QSpinBox:hover {
            border: 1px solid #6750A4;
        }
        
        QSpinBox::up-button, QSpinBox::down-button {
            width: 16px;
            border-radius: 2px;
            background-color: #3A3A3A;
        }
        
        QSpinBox::up-button:hover, QSpinBox::down-button:hover {
            background-color: #6750A4;
        }
        
        QLabel#speedValueLabel {
            color: #D0BCFF;
            font-weight: bold;
            font-size: 14px;
        }
        
        QLabel#smoothLabel {
            color: #E1E1E1;
            padding-right: 0px;
        }
    """