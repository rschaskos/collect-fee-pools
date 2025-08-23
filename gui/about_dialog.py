from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                               QPushButton, QFrame, QScrollArea, QWidget)
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QFont, QPixmap, QDesktopServices
import sys
import platform

class AboutDialog(QDialog):
    """Diálogo com informações sobre a aplicação."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """Configura a interface do diálogo About."""
        self.setWindowTitle("Sobre - Monitor de Coletas")
        self.setModal(True)
        self.setFixedSize(520, 620)
        
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Área de scroll
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        
        # Widget de conteúdo
        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(25, 25, 25, 25)
        
        # Cabeçalho
        self.criar_cabecalho(layout)
        
        # Separador
        self.adicionar_separador(layout)
        
        # Informações da aplicação
        self.criar_info_aplicacao(layout)
        
        # Separador
        self.adicionar_separador(layout)
        
        # Informações técnicas
        self.criar_info_tecnica(layout)
        
        # Separador
        self.adicionar_separador(layout)
        
        # Desenvolvedor
        self.criar_info_desenvolvedor(layout)
        
        # Configurar scroll
        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)
        
        # Botões fixos na parte inferior
        self.criar_botoes(main_layout)
    
    def adicionar_separador(self, layout):
        """Adiciona um separador visual."""
        separador = QFrame()
        separador.setFrameShape(QFrame.HLine)
        separador.setFrameShadow(QFrame.Sunken)
        separador.setStyleSheet("color: #bdc3c7;")
        layout.addWidget(separador)
    
    def criar_cabecalho(self, layout):
        """Cria o cabeçalho com ícone e título."""
        # Ícone da aplicação
        icone_label = QLabel("🏊‍♂️")
        icone_font = QFont()
        icone_font.setPointSize(48)
        icone_label.setFont(icone_font)
        icone_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(icone_label)
        
        # Título da aplicação
        titulo_label = QLabel("Monitor de Coletas")
        titulo_font = QFont()
        titulo_font.setPointSize(20)
        titulo_font.setBold(True)
        titulo_label.setFont(titulo_font)
        titulo_label.setAlignment(Qt.AlignCenter)
        titulo_label.setStyleSheet("color: #2c3e50; margin: 5px 0;")
        layout.addWidget(titulo_label)
        
        # Subtítulo
        subtitulo_label = QLabel("Pools de Liquidez")
        subtitulo_font = QFont()
        subtitulo_font.setPointSize(14)
        subtitulo_label.setFont(subtitulo_font)
        subtitulo_label.setAlignment(Qt.AlignCenter)
        subtitulo_label.setStyleSheet("color: #7f8c8d; margin-bottom: 10px;")
        layout.addWidget(subtitulo_label)
    
    def criar_info_aplicacao(self, layout):
        """Cria seção com informações da aplicação."""
        # Título da seção
        titulo = QLabel("📱 Informações da Aplicação")
        titulo_font = QFont()
        titulo_font.setPointSize(14)
        titulo_font.setBold(True)
        titulo.setFont(titulo_font)
        titulo.setStyleSheet("color: #34495e; margin-bottom: 15px;")
        layout.addWidget(titulo)
        
        # Versão
        versao_label = QLabel("Versão: 2.0.0")
        versao_label.setStyleSheet("font-size: 13px; color: #2c3e50; margin-bottom: 8px;")
        layout.addWidget(versao_label)
        
        # Descrição
        desc_label = QLabel("Aplicação moderna para monitorar coletas de taxas de múltiplas pools de liquidez DeFi.")
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("font-size: 13px; color: #2c3e50; margin-bottom: 15px; line-height: 1.4;")
        layout.addWidget(desc_label)
        
        # Funcionalidades
        func_titulo = QLabel("Principais Funcionalidades:")
        func_titulo.setStyleSheet("font-size: 13px; font-weight: bold; color: #2c3e50; margin-bottom: 5px;")
        layout.addWidget(func_titulo)
        
        funcionalidades = [
            "• Gerenciamento de múltiplas pools simultâneas",
            "• Cálculo automático de taxas baseado no valor inicial",
            "• Histórico completo de coletas com totais acumulados",
            "• Exportação de dados em formato CSV",
            "• Interface moderna e intuitiva"
        ]
        
        for func in funcionalidades:
            func_label = QLabel(func)
            func_label.setStyleSheet("font-size: 12px; color: #34495e; margin-left: 10px; margin-bottom: 3px;")
            layout.addWidget(func_label)
    
    def criar_info_tecnica(self, layout):
        """Cria seção com informações técnicas."""
        # Título da seção
        titulo = QLabel("⚙️ Tecnologias Utilizadas")
        titulo_font = QFont()
        titulo_font.setPointSize(14)
        titulo_font.setBold(True)
        titulo.setFont(titulo_font)
        titulo.setStyleSheet("color: #34495e; margin-bottom: 15px;")
        layout.addWidget(titulo)
        
        # Informações do sistema
        python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        sistema = platform.system()
        arquitetura = platform.machine()
        
        tech_items = [
            ("🐍 Python:", python_version),
            ("🖼️ Interface Gráfica:", "PySide6 (Qt6)"),
            ("💾 Persistência:", "CSV Files"),
            ("🔧 Build:", "PyInstaller"),
            ("💻 Sistema:", f"{sistema} ({arquitetura})"),
            ("🏗️ Arquitetura:", "MVC Pattern")
        ]
        
        for label_text, value_text in tech_items:
            item_layout = QHBoxLayout()
            item_layout.setSpacing(10)
            
            label = QLabel(label_text)
            label.setStyleSheet("font-size: 12px; font-weight: bold; color: #2c3e50; min-width: 140px;")
            
            value = QLabel(value_text)
            value.setStyleSheet("font-size: 12px; color: #7f8c8d;")
            
            item_layout.addWidget(label)
            item_layout.addWidget(value)
            item_layout.addStretch()
            
            layout.addLayout(item_layout)
    
    def criar_info_desenvolvedor(self, layout):
        """Cria seção com informações do desenvolvedor."""
        # Título da seção
        titulo = QLabel("👨‍💻 Desenvolvedor")
        titulo_font = QFont()
        titulo_font.setPointSize(14)
        titulo_font.setBold(True)
        titulo.setFont(titulo_font)
        titulo.setStyleSheet("color: #34495e; margin-bottom: 15px;")
        layout.addWidget(titulo)
        
        dev_items = [
            ("📝 Criado por:", "Rschaskos"),  # Altere aqui seu nome
            ("🎯 Objetivo:", "Facilitar o monitoramento de pools DeFi"),
            ("📅 Desenvolvido em:", "Agosto 2025")
        ]
        
        for label_text, value_text in dev_items:
            item_layout = QHBoxLayout()
            item_layout.setSpacing(10)
            
            label = QLabel(label_text)
            label.setStyleSheet("font-size: 12px; font-weight: bold; color: #2c3e50; min-width: 140px;")
            
            value = QLabel(value_text)
            value.setStyleSheet("font-size: 12px; color: #7f8c8d;")
            
            item_layout.addWidget(label)
            item_layout.addWidget(value)
            item_layout.addStretch()
            
            layout.addLayout(item_layout)
        
        # Mensagem especial
        mensagem_label = QLabel("Desenvolvido para a comunidade DeFi 🚀")
        mensagem_label.setAlignment(Qt.AlignCenter)
        mensagem_label.setStyleSheet("""
            color: #27ae60; 
            font-weight: bold; 
            font-style: italic; 
            margin: 20px 0 10px 0;
            padding: 15px;
            background-color: #d5f4e6;
            border-radius: 8px;
            font-size: 14px;
        """)
        layout.addWidget(mensagem_label)
    
    def criar_botoes(self, layout):
        """Cria os botões do diálogo."""
        # Container para botões
        botoes_container = QWidget()
        botoes_container.setStyleSheet("background-color: #f8f9fa; border-top: 1px solid #dee2e6;")
        botoes_layout = QHBoxLayout(botoes_container)
        botoes_layout.setContentsMargins(20, 15, 20, 15)
        
        # Botão GitHub (opcional)
        self.btn_github = QPushButton("📂 Código Fonte")
        self.btn_github.clicked.connect(self.abrir_github)
        self.btn_github.setStyleSheet("""
            QPushButton {
                background-color: #6f42c1;
                color: white;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover {
                background-color: #5a2d91;
            }
        """)
        botoes_layout.addWidget(self.btn_github)
        
        botoes_layout.addStretch()
        
        # Botão Fechar
        self.btn_fechar = QPushButton("Fechar")
        self.btn_fechar.clicked.connect(self.accept)
        self.btn_fechar.setDefault(True)
        self.btn_fechar.setStyleSheet("""
            QPushButton {
                background-color: #34495e;
                color: white;
                padding: 10px 25px;
                border-radius: 6px;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover {
                background-color: #2c3e50;
            }
        """)
        botoes_layout.addWidget(self.btn_fechar)
        
        layout.addWidget(botoes_container)
    
    def abrir_github(self):
        """Abre o GitHub no navegador (opcional)."""
        # Você pode alterar este URL para seu repositório
        url = "https://github.com/rschaskos/collect-fee-pools"  
        QDesktopServices.openUrl(QUrl(url))