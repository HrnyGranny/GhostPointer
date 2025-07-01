def get_app_styles():
    return """
        QWidget {
            background-color: #121212;
            color: #E1E1E1;
            font-family: 'Segoe UI', 'Roboto', sans-serif;
            font-size: 12px;
        }
        
        /* Botones de opción principales */
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
        
        /* Botones compactos (del tab de clics) */
        QPushButton#compactButton {
            background-color: #1E1E1E;
            color: #E1E1E1;
            border: 1px solid #31303A;
            border-radius: 6px;
            padding: 2px 4px;
            font-size: 11px;
            min-width: 60px;
        }
        
        QPushButton#compactButton:hover {
            background-color: #2A2A2A;
            border: 1px solid #6750A4;
        }
        
        QPushButton#compactButton:checked {
            background-color: #31303A;
            border: 1px solid #6750A4;
            color: #D0BCFF;
        }
        
        /* Radio Buttons */
        QRadioButton {
            color: #E1E1E1;
            font-size: 11px;
        }
        
        QRadioButton::indicator {
            width: 12px;
            height: 12px;
            border-radius: 6px;
        }
        
        QRadioButton::indicator:unchecked {
            background-color: #2A2A2A;
            border: 1px solid #3A3A3A;
        }
        
        QRadioButton::indicator:checked {
            background-color: #6750A4;
            border: 1px solid #D0BCFF;
        }
        
        /* Sliders */
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
        
        /* Frames */
        QFrame#optionsFrameWithBg {
            border: 1px solid #31303A;
            border-radius: 10px;
            background-color: #1A1A1A;
        }
        
        QFrame#transparentFrame {
            border: none;
            background-color: transparent;
        }
        
        /* Checkboxes */
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
        
        /* Labels */
        QLabel#shortcutLabel {
            color: #8F8F8F;
            font-size: 11px;
            font-style: italic;
            font-weight: 400;
            margin-top: 4px;
        }
        
        QLabel#speedValueLabel {
            color: #D0BCFF;
            font-weight: bold;
            font-size: 14px;
        }
        
        QLabel#stopLabel {
            color: #E1E1E1;
            padding-right: 0px;
        }
        
        QLabel#sectionLabel {
            color: #E1E1E1;
            font-weight: 500;
        }
        
        /* Console output */
        #consoleOutput {
            background-color: #1A1A1A;
            border: 1px solid #31303A;
            border-radius: 8px;
            color: #E1E1E1;
            font-family: 'Consolas', 'Courier New', monospace;
            font-size: 11px;
            padding: 8px;
        }
        
        /* SpinBoxes */
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
        
        QSpinBox:disabled {
            background-color: #1A1A1A;
            color: #5A5A5A;
            border: 1px solid #2A2A2A;
        }
        
        QSpinBox::up-button, QSpinBox::down-button {
            width: 16px;
            border-radius: 2px;
            background-color: #3A3A3A;
        }
        
        QSpinBox::up-button:hover, QSpinBox::down-button:hover {
            background-color: #6750A4;
        }
        
        /* Counter styles */
        #counterWidget {
            background-color: #1e1e1e;
            border-top: 1px solid #333;
        }

        #counterWidget QLabel {
            color: #e0e0e0;
            font-size: 11px;
            border: none;
            padding: 0px;
            margin: 0px;
            background: transparent;
        }
        
        #counterDisplay {
            color: #D0BCFF;
            font-weight: bold;
            font-family: 'Consolas', 'Courier New', monospace;
            border: none;
            padding: 0px;
            margin: 0px;
            background: transparent;
        }
    """