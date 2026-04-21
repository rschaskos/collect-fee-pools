from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                               QPushButton)
from PySide6.QtCore import Qt, QUrl, QSize
from PySide6.QtGui import QFont, QDesktopServices
from utils.icons import get_icon

class AboutDialog(QDialog):
    """Diálogo com informações sobre a aplicação."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        """Configura a interface do diálogo About."""
        self.setWindowTitle("Sobre")
        self.setModal(True)
        self.setFixedSize(500, 340)

        # Layout principal
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)

        # Título da aplicação
        titulo_label = QLabel("Monitor de Coletas")
        titulo_font = QFont()
        titulo_font.setPointSize(18)
        titulo_font.setBold(True)
        titulo_label.setFont(titulo_font)
        titulo_label.setAlignment(Qt.AlignCenter)
        titulo_label.setStyleSheet("color: #2c3e50;")
        layout.addWidget(titulo_label)

        # Subtítulo
        subtitulo_label = QLabel("Pools de Liquidez")
        subtitulo_font = QFont()
        subtitulo_font.setPointSize(12)
        subtitulo_label.setFont(subtitulo_font)
        subtitulo_label.setAlignment(Qt.AlignCenter)
        subtitulo_label.setStyleSheet("color: #7f8c8d;")
        layout.addWidget(subtitulo_label)

        # Espaço em branco
        layout.addSpacing(10)

        # Versão
        versao_label = QLabel("Version 2.0.0")
        versao_label.setAlignment(Qt.AlignCenter)
        versao_label.setStyleSheet("color: #2c3e50;")
        layout.addWidget(versao_label)

        # Espaço em branco
        layout.addSpacing(10)

        # Descrição
        desc_label = QLabel("Modern application for monitoring fee collections from DeFi pools.")
        desc_label.setWordWrap(True)
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setStyleSheet("color: #2c3e50;")
        layout.addWidget(desc_label)

        # Stretch para empurrar o rodapé para baixo
        layout.addStretch()

        # Rodapé com copyright
        copyright_label = QLabel("© 2025 Rschaskos")
        copyright_font = QFont()
        copyright_font.setPointSize(10)
        copyright_label.setFont(copyright_font)
        copyright_label.setAlignment(Qt.AlignCenter)
        copyright_label.setStyleSheet("color: #7f8c8d;")
        layout.addWidget(copyright_label)

        # Espaço antes dos botões
        layout.addSpacing(10)

        # Botões
        botoes_layout = QHBoxLayout()

        # Botão Source Code
        self.btn_source = QPushButton("Source Code")
        self.btn_source.setIcon(get_icon("github"))
        self.btn_source.setIconSize(QSize(18, 18))
        self.btn_source.clicked.connect(self.abrir_github)
        self.btn_source.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #2c3e50;
                padding: 8px 15px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #f8f9fa;
            }
        """)
        botoes_layout.addWidget(self.btn_source)

        # Botão Close
        self.btn_close = QPushButton("Close")
        self.btn_close.clicked.connect(self.accept)
        self.btn_close.setDefault(True)
        self.btn_close.setStyleSheet("""
            QPushButton {
                background-color: #2c3e50;
                color: white;
                padding: 8px 20px;
                border-radius: 4px;
                border: none;
            }
            QPushButton:hover {
                background-color: #34495e;
            }
        """)
        botoes_layout.addWidget(self.btn_close)

        layout.addLayout(botoes_layout)

    def abrir_github(self):
        """Abre o GitHub no navegador."""
        url = "https://github.com/rschaskos/collect-fee-pools"
        QDesktopServices.openUrl(QUrl(url))