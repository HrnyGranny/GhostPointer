from PyQt6.QtWidgets import QTextEdit

class ConsoleOutput(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.setObjectName("consoleOutput")
        self.setMinimumHeight(120)
        self.setMaximumHeight(200)
        
    def log(self, message):
        """Add a message to the console"""
        self.append(f"> {message}")

    def show_banner(self):
        """Muestra un banner compacto y estilizado en la consola"""
        import datetime
        
        # Obtener fecha actual
        current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        version = "1.2.0"
        
        # Banner compacto con colores HTML
        banner = f"""<pre style="color:#6750A4; font-family:'Consolas', 'Courier New'">
        ╭────────── <span style="color:#D0BCFF; font-weight:bold">Ghost Pointer</span> ──────────╮
        │ <span style="color:#B0B0B0">v{version}</span>          <span style="color:#B0B0B0">{current_date}</span>  │
        │ <span style="color:#E1E1E1">Developer mode</span>       <span style="color:#B0B0B0">@HrnyGranny</span>  │
        ╰───────────────────────────────────╯</pre>
    """
        
        # Limpiar consola primero
        self.clear()
        
        # Mostrar banner
        self.insertHtml(banner)