import sys
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                               QPushButton, QTableWidget, QTableWidgetItem, QLabel,
                               QMessageBox, QFileDialog, QComboBox, QFrame, QDialog,
                               QMenuBar, QMenu, QGridLayout, QSizePolicy)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QSize
from PySide6.QtGui import QFont, QIcon, QPalette, QAction

from core.monitor import MonitorLiquidez
from gui.dialogs import PoolConfigDialog, NovaColetaDialog, SelecionarPoolDialog, EditarColetaDialog
from gui.about_dialog import AboutDialog
from utils.icons import get_icon

# Importar estilos (precisa criar o arquivo utils/styles.py)
try:
    from utils.styles import ModernStyles
except ImportError:
    # Fallback se o arquivo não existir ainda
    class ModernStyles:
        @staticmethod
        def get_button_style(color_type='primary', size='medium'):
            return ""
        @staticmethod
        def get_card_style(elevated=True):
            return ""
        @staticmethod
        def get_table_style():
            return ""
        @staticmethod
        def get_combo_style():
            return ""
        @staticmethod
        def get_stats_card_style(color_type='primary'):
            return ""

class MonitorColetasApp(QMainWindow):
    """Janela principal da aplicação."""
    
    def __init__(self):
        super().__init__()
        self.monitor = MonitorLiquidez()
        self.setup_ui()
        self.criar_menu()
        self.atualizar_interface()
    
    def criar_menu(self):
        """Cria a barra de menu."""
        menubar = self.menuBar()
        
        # Menu Arquivo
        menu_arquivo = menubar.addMenu("Arquivo")
        
        # Ação Nova Pool
        acao_nova_pool = QAction("Nova Pool", self)
        acao_nova_pool.setShortcut("Ctrl+N")
        acao_nova_pool.setStatusTip("Criar uma nova pool de liquidez")
        acao_nova_pool.triggered.connect(self.nova_pool)
        menu_arquivo.addAction(acao_nova_pool)
        
        # Ação Nova Coleta
        acao_nova_coleta = QAction("Nova Coleta", self)
        acao_nova_coleta.setShortcut("Ctrl+R")
        acao_nova_coleta.setStatusTip("Registrar nova coleta na pool ativa")
        acao_nova_coleta.triggered.connect(self.nova_coleta)
        menu_arquivo.addAction(acao_nova_coleta)
        
        menu_arquivo.addSeparator()
        
        # Ação Exportar
        acao_exportar = QAction("Exportar CSV", self)
        acao_exportar.setShortcut("Ctrl+E")
        acao_exportar.setStatusTip("Exportar dados da pool ativa")
        acao_exportar.triggered.connect(self.exportar_dados)
        menu_arquivo.addAction(acao_exportar)
        
        menu_arquivo.addSeparator()
        
        # Ação Sair
        acao_sair = QAction("Sair", self)
        acao_sair.setShortcut("Ctrl+Q")
        acao_sair.setStatusTip("Sair da aplicação")
        acao_sair.triggered.connect(self.close)
        menu_arquivo.addAction(acao_sair)
        
        # Menu Pools
        menu_pools = menubar.addMenu("Pools")
        
        # Ação Editar Pool
        acao_editar_pool = QAction("Editar Pool Ativa", self)
        acao_editar_pool.setShortcut("Ctrl+Alt+E")
        acao_editar_pool.triggered.connect(self.editar_pool)
        menu_pools.addAction(acao_editar_pool)
        
        # Ação Excluir Pool
        acao_excluir_pool = QAction("Excluir Pool", self)
        acao_excluir_pool.setShortcut("Ctrl+Alt+D")
        acao_excluir_pool.triggered.connect(self.excluir_pool)
        menu_pools.addAction(acao_excluir_pool)
        
        menu_pools.addSeparator()
        
        # Ação Limpar Dados
        acao_limpar = QAction("Limpar Dados da Pool", self)
        acao_limpar.triggered.connect(self.limpar_dados)
        menu_pools.addAction(acao_limpar)
        
        # Menu Ajuda
        menu_ajuda = menubar.addMenu("Ajuda")
        
        # Ação Sobre
        acao_sobre = QAction("Sobre", self)
        acao_sobre.setShortcut("F1")
        acao_sobre.setStatusTip("Informações sobre a aplicação")
        acao_sobre.triggered.connect(self.mostrar_sobre)
        menu_ajuda.addAction(acao_sobre)
        
        # Ação Atalhos
        acao_atalhos = QAction("Atalhos do Teclado", self)
        acao_atalhos.triggered.connect(self.mostrar_atalhos)
        menu_ajuda.addAction(acao_atalhos)
    
    def mostrar_sobre(self):
        """Mostra o diálogo sobre a aplicação."""
        dialog = AboutDialog(self)
        dialog.exec()
    
    def mostrar_atalhos(self):
        """Mostra os atalhos de teclado disponíveis."""
        atalhos_text = """
        <h3>Atalhos de Teclado</h3>
        <table style="border-collapse: collapse; width: 100%;">
        <tr><td style="padding: 5px; font-weight: bold;">Ctrl+N</td><td style="padding: 5px;">Nova Pool</td></tr>
        <tr><td style="padding: 5px; font-weight: bold;">Ctrl+R</td><td style="padding: 5px;">Nova Coleta</td></tr>
        <tr><td style="padding: 5px; font-weight: bold;">Ctrl+E</td><td style="padding: 5px;">Exportar CSV</td></tr>
        <tr><td style="padding: 5px; font-weight: bold;">Ctrl+Alt+E</td><td style="padding: 5px;">Editar Pool Ativa</td></tr>
        <tr><td style="padding: 5px; font-weight: bold;">Ctrl+Alt+D</td><td style="padding: 5px;">Excluir Pool</td></tr>
        <tr><td style="padding: 5px; font-weight: bold;">F1</td><td style="padding: 5px;">Sobre</td></tr>
        <tr><td style="padding: 5px; font-weight: bold;">Ctrl+Q</td><td style="padding: 5px;">Sair</td></tr>
        </table>
        """
        
        QMessageBox.about(self, "Atalhos de Teclado", atalhos_text)
    
    def setup_ui(self):
        """Configura a interface principal - VERSÃO COM ESPAÇAMENTO OTIMIZADO."""
        self.setWindowTitle("Monitor de Coletas - Pools de Liquidez")
        
        # === JANELA COM ALTURA ADEQUADA ===
        self.resize(1000, 750)  # ← ALTURA AUMENTADA de 700 para 750
        self.setMinimumSize(900, 700)  # ← ALTURA MÍNIMA AUMENTADA de 600 para 700
        self.move(200, 50)  # ← Y menor para começar mais alto
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Garantir que todos os controles de janela estão disponíveis
        from PySide6.QtCore import Qt
        self.setWindowFlags(
            Qt.Window | 
            Qt.WindowTitleHint | 
            Qt.WindowCloseButtonHint | 
            Qt.WindowMinimizeButtonHint | 
            Qt.WindowMaximizeButtonHint |
            Qt.WindowSystemMenuHint
        )
        
        # === INTERFACE COM ESPAÇAMENTOS REDUZIDOS ===
        
        # Cor de fundo moderna
        self.setStyleSheet("""
            QMainWindow {
                background-color: #F8FAFC;
            }
        """)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal com ESPAÇAMENTOS MENORES
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(16)  # ← REDUZIDO de 24 para 16
        layout.setContentsMargins(20, 20, 20, 20)  # ← REDUZIDO de 24 para 20
        
        # Cabeçalho MENOR
        self.criar_cabecalho_compacto(layout)
        
        # Cards de estatísticas (já funcionando)
        self.criar_cards_estatisticas(layout)
        
        # Seção de controle de pools COMPACTA
        self.criar_secao_pools_compacta(layout)
        
        # Seção de coletas COMPACTA
        self.criar_secao_coletas_compacta(layout)
        
        # Tabela de dados (deve ocupar o espaço restante)
        self.criar_tabela(layout)

    def criar_cabecalho_compacto(self, layout):
        """Cria cabeçalho mais compacto."""
        header_frame = QFrame()
        header_frame.setFixedHeight(160)  # ← ALTURA FIXA MENOR
        header_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3B82F6, stop:1 #6366F1);
                border-radius: 12px;
                padding: 16px;
            }
        """)
        
        header_layout = QVBoxLayout(header_frame)
        header_layout.setSpacing(4)
        header_layout.setAlignment(Qt.AlignCenter)
        
        # Título principal MENOR
        titulo_label = QLabel("Monitor de Coletas")
        titulo_font = QFont()
        titulo_font.setPointSize(20)  # ← REDUZIDO de 24 para 20
        titulo_font.setBold(True)
        titulo_label.setFont(titulo_font)
        titulo_label.setAlignment(Qt.AlignCenter)
        titulo_label.setStyleSheet("color: white; margin: 0;")
        header_layout.addWidget(titulo_label)
        
        # Subtítulo MENOR
        subtitulo_label = QLabel("Pools de Liquidez DeFi")
        subtitulo_font = QFont()
        subtitulo_font.setPointSize(12)  # ← REDUZIDO de 14 para 12
        subtitulo_label.setFont(subtitulo_font)
        subtitulo_label.setAlignment(Qt.AlignCenter)
        subtitulo_label.setStyleSheet("color: rgba(255,255,255,0.9); margin: 0;")
        header_layout.addWidget(subtitulo_label)
        
        layout.addWidget(header_frame)

    def criar_secao_pools_compacta(self, layout):
        """Cria seção de pools mais compacta."""
        pools_card = QFrame()
        pools_card.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #E5E7EB;
                border-radius: 8px;
                padding: 12px;  
            }
        """)
        
        pools_layout = QVBoxLayout(pools_card)
        pools_layout.setSpacing(12)  # ← REDUZIDO de 16 para 12
        
        # Título da seção MENOR
        titulo_label = QLabel("Gerenciamento de Pools")
        titulo_font = QFont()
        titulo_font.setPointSize(14)  # ← REDUZIDO de 16 para 14
        titulo_font.setBold(True)
        titulo_label.setFont(titulo_font)
        titulo_label.setStyleSheet("color: #1F2937; margin: 0;")
        pools_layout.addWidget(titulo_label)
        
        # Controles em uma linha
        controles_layout = QHBoxLayout()
        controles_layout.setSpacing(10)
        
        # Label e dropdown
        pool_label = QLabel("Pool Ativa:")
        pool_label.setStyleSheet("font-weight: 600; color: #374151; font-size: 13px;")
        controles_layout.addWidget(pool_label)
        
        self.combo_pools = QComboBox()
        self.combo_pools.setMinimumWidth(250)  # ← REDUZIDO de 300 para 250
        self.combo_pools.currentTextChanged.connect(self.pool_selecionada_mudou)
        self.combo_pools.setStyleSheet("""
            QComboBox {
                background-color: white;
                border: 1px solid #D1D5DB;
                border-radius: 6px;
                padding: 6px 10px;
                font-size: 13px;
                color: #1F2937;
            }
            QComboBox:hover {
                border-color: #3B82F6;
            }
        """)
        controles_layout.addWidget(self.combo_pools)
        
        controles_layout.addStretch()
        
        # Botões MENORES
        self.btn_nova_pool = QPushButton("Nova Pool")
        self.btn_nova_pool.setIcon(get_icon("plus"))
        self.btn_nova_pool.setIconSize(QSize(18, 18))
        self.btn_nova_pool.clicked.connect(self.nova_pool)
        self.btn_nova_pool.setStyleSheet("""
            QPushButton {
                background-color: #10B981;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 14px;
                font-weight: 600;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #059669;
            }
        """)
        controles_layout.addWidget(self.btn_nova_pool)
        
        self.btn_editar_pool = QPushButton("Editar")
        self.btn_editar_pool.setIcon(get_icon("edit"))
        self.btn_editar_pool.setIconSize(QSize(18, 18))
        self.btn_editar_pool.clicked.connect(self.editar_pool)
        self.btn_editar_pool.setStyleSheet("""
            QPushButton {
                background-color: #3B82F6;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 14px;
                font-weight: 600;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #2563EB;
            }
        """)
        controles_layout.addWidget(self.btn_editar_pool)
        
        self.btn_excluir_pool = QPushButton("Excluir")
        self.btn_excluir_pool.setIcon(get_icon("trash"))
        self.btn_excluir_pool.setIconSize(QSize(18, 18))
        self.btn_excluir_pool.clicked.connect(self.excluir_pool)
        self.btn_excluir_pool.setStyleSheet("""
            QPushButton {
                background-color: #EF4444;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 14px;
                font-weight: 600;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #DC2626;
            }
        """)
        controles_layout.addWidget(self.btn_excluir_pool)
        
        pools_layout.addLayout(controles_layout)
        layout.addWidget(pools_card)

    def criar_secao_coletas_compacta(self, layout):
        """Cria seção de coletas mais compacta."""
        coletas_card = QFrame()
        coletas_card.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #E5E7EB;
                border-radius: 8px;
                padding: 12px;
            }
        """)
        
        coletas_layout = QVBoxLayout(coletas_card)
        coletas_layout.setSpacing(12)  # ← REDUZIDO
        
        # Título da seção MENOR
        titulo_label = QLabel("Coletas da Pool Ativa")
        titulo_font = QFont()
        titulo_font.setPointSize(14)  # ← REDUZIDO de 16 para 14
        titulo_font.setBold(True)
        titulo_label.setFont(titulo_font)
        titulo_label.setStyleSheet("color: #1F2937; margin: 0;")
        coletas_layout.addWidget(titulo_label)
        
        # Botões de ação MENORES
        acoes_layout = QHBoxLayout()
        acoes_layout.setSpacing(10)
        
        self.btn_nova_coleta = QPushButton("Nova Coleta")
        self.btn_nova_coleta.setIcon(get_icon("plus"))
        self.btn_nova_coleta.setIconSize(QSize(18, 18))
        self.btn_nova_coleta.clicked.connect(self.nova_coleta)
        self.btn_nova_coleta.setStyleSheet("""
            QPushButton {
                background-color: #10B981;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 16px;
                font-weight: 600;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #059669;
            }
        """)
        acoes_layout.addWidget(self.btn_nova_coleta)
        
        acoes_layout.addStretch()
        
        self.btn_exportar = QPushButton("Exportar CSV")
        self.btn_exportar.setIcon(get_icon("chart"))
        self.btn_exportar.setIconSize(QSize(18, 18))
        self.btn_exportar.clicked.connect(self.exportar_dados)
        self.btn_exportar.setStyleSheet("""
            QPushButton {
                background-color: #6366F1;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 14px;
                font-weight: 600;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #4F46E5;
            }
        """)
        acoes_layout.addWidget(self.btn_exportar)
        
        self.btn_limpar = QPushButton("Limpar Dados")
        self.btn_limpar.setIcon(get_icon("trash"))
        self.btn_limpar.setIconSize(QSize(18, 18))
        self.btn_limpar.clicked.connect(self.limpar_dados)
        self.btn_limpar.setStyleSheet("""
            QPushButton {
                background-color: #F59E0B;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 14px;
                font-weight: 600;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #D97706;
            }
        """)
        acoes_layout.addWidget(self.btn_limpar)
        
        coletas_layout.addLayout(acoes_layout)
        layout.addWidget(coletas_card)
    
    
    def criar_cards_estatisticas(self, layout):
        """Cria cards com estatísticas principais - VERSÃO FINAL CORRIGIDA."""
        
        stats_frame = QFrame()
        stats_frame.setStyleSheet("QFrame { background-color: transparent; }")
        
        # Layout horizontal com stretch
        stats_layout = QHBoxLayout(stats_frame)
        stats_layout.setSpacing(16)
        stats_layout.setContentsMargins(0, 0, 0, 0)
        
        # === CARD 1: TOTAL COLETAS ===
        self.card_total_coletas = QFrame()
        self.card_total_coletas.setFixedSize(220, 140)  # ← TAMANHO FIXO
        self.card_total_coletas.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 2px solid #3B82F6;
                border-radius: 12px;
                padding: 0px;
                margin: 4px;
            }
        """)
        
        # Layout interno com margens controladas
        layout1 = QVBoxLayout(self.card_total_coletas)
        layout1.setContentsMargins(16, 16, 16, 16)
        layout1.setSpacing(8)
        
        # Header fixo
        header1 = QLabel("Total de Coletas")
        header1.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            color: #3B82F6;
            background-color: transparent;
            border: none;
            padding: 0px;
            margin: 0px;
        """)
        header1.setAlignment(Qt.AlignLeft)
        header1.setFixedHeight(20)  # ← ALTURA FIXA
        layout1.addWidget(header1)
        
        # Valor principal com altura fixa
        self.card_total_coletas.valor_label = QLabel("0")
        self.card_total_coletas.valor_label.setStyleSheet("""
            font-size: 28px; 
            font-weight: bold; 
            color: #1F2937;
            background-color: transparent;
            border: none;
            padding: 0px;
            margin: 0px;
        """)
        self.card_total_coletas.valor_label.setAlignment(Qt.AlignLeft)
        self.card_total_coletas.valor_label.setFixedHeight(35)  # ← ALTURA FIXA
        layout1.addWidget(self.card_total_coletas.valor_label)
        
        # Descrição com altura fixa
        self.card_total_coletas.desc_label = QLabel("Coletas registradas")
        self.card_total_coletas.desc_label.setStyleSheet("""
            font-size: 12px; 
            color: #6B7280;
            background-color: transparent;
            border: none;
            padding: 0px;
            margin: 0px;
        """)
        self.card_total_coletas.desc_label.setAlignment(Qt.AlignLeft)
        self.card_total_coletas.desc_label.setFixedHeight(15)  # ← ALTURA FIXA
        layout1.addWidget(self.card_total_coletas.desc_label)
        
        # Stretch para empurrar tudo para cima
        layout1.addStretch()
        
        stats_layout.addWidget(self.card_total_coletas)
        
        # === CARD 2: TOTAL ACUMULADO ===
        self.card_total_acumulado = QFrame()
        self.card_total_acumulado.setFixedSize(220, 140)  # ← TAMANHO FIXO
        self.card_total_acumulado.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 2px solid #10B981;
                border-radius: 12px;
                padding: 0px;
                margin: 4px;
            }
        """)
        
        layout2 = QVBoxLayout(self.card_total_acumulado)
        layout2.setContentsMargins(16, 16, 16, 16)
        layout2.setSpacing(8)
        
        header2 = QLabel("Total Acumulado")
        header2.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            color: #10B981;
            background-color: transparent;
            border: none;
            padding: 0px;
            margin: 0px;
        """)
        header2.setAlignment(Qt.AlignLeft)
        header2.setFixedHeight(20)
        layout2.addWidget(header2)
        
        self.card_total_acumulado.valor_label = QLabel("$0.00")
        self.card_total_acumulado.valor_label.setStyleSheet("""
            font-size: 28px; 
            font-weight: bold; 
            color: #1F2937;
            background-color: transparent;
            border: none;
            padding: 0px;
            margin: 0px;
        """)
        self.card_total_acumulado.valor_label.setAlignment(Qt.AlignLeft)
        self.card_total_acumulado.valor_label.setFixedHeight(35)
        layout2.addWidget(self.card_total_acumulado.valor_label)
        
        self.card_total_acumulado.desc_label = QLabel("Valor total coletado")
        self.card_total_acumulado.desc_label.setStyleSheet("""
            font-size: 12px; 
            color: #6B7280;
            background-color: transparent;
            border: none;
            padding: 0px;
            margin: 0px;
        """)
        self.card_total_acumulado.desc_label.setAlignment(Qt.AlignLeft)
        self.card_total_acumulado.desc_label.setFixedHeight(15)
        layout2.addWidget(self.card_total_acumulado.desc_label)
        
        layout2.addStretch()
        stats_layout.addWidget(self.card_total_acumulado)
        
        # === CARD 3: TAXA ACUMULADA ===
        self.card_taxa_acumulada = QFrame()
        self.card_taxa_acumulada.setFixedSize(220, 140)  # ← TAMANHO FIXO
        self.card_taxa_acumulada.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 2px solid #F59E0B;
                border-radius: 12px;
                padding: 0px;
                margin: 4px;
            }
        """)
        
        layout3 = QVBoxLayout(self.card_taxa_acumulada)
        layout3.setContentsMargins(16, 16, 16, 16)
        layout3.setSpacing(8)
        
        header3 = QLabel("Taxa Acumulada")
        header3.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            color: #F59E0B;
            background-color: transparent;
            border: none;
            padding: 0px;
            margin: 0px;
        """)
        header3.setAlignment(Qt.AlignLeft)
        header3.setFixedHeight(20)
        layout3.addWidget(header3)
        
        self.card_taxa_acumulada.valor_label = QLabel("0.00%")
        self.card_taxa_acumulada.valor_label.setStyleSheet("""
            font-size: 28px; 
            font-weight: bold; 
            color: #1F2937;
            background-color: transparent;
            border: none;
            padding: 0px;
            margin: 0px;
        """)
        self.card_taxa_acumulada.valor_label.setAlignment(Qt.AlignLeft)
        self.card_taxa_acumulada.valor_label.setFixedHeight(35)
        layout3.addWidget(self.card_taxa_acumulada.valor_label)
        
        self.card_taxa_acumulada.desc_label = QLabel("Taxa percentual total")
        self.card_taxa_acumulada.desc_label.setStyleSheet("""
            font-size: 12px; 
            color: #6B7280;
            background-color: transparent;
            border: none;
            padding: 0px;
            margin: 0px;
        """)
        self.card_taxa_acumulada.desc_label.setAlignment(Qt.AlignLeft)
        self.card_taxa_acumulada.desc_label.setFixedHeight(15)
        layout3.addWidget(self.card_taxa_acumulada.desc_label)
        
        layout3.addStretch()
        stats_layout.addWidget(self.card_taxa_acumulada)
        
        # === CARD 4: MÉDIA POR COLETA ===
        self.card_media_coleta = QFrame()
        self.card_media_coleta.setFixedSize(220, 140)  # ← TAMANHO FIXO
        self.card_media_coleta.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 2px solid #EF4444;
                border-radius: 12px;
                padding: 0px;
                margin: 4px;
            }
        """)
        
        layout4 = QVBoxLayout(self.card_media_coleta)
        layout4.setContentsMargins(16, 16, 16, 16)
        layout4.setSpacing(8)
        
        header4 = QLabel("Média por Coleta")
        header4.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            color: #EF4444;
            background-color: transparent;
            border: none;
            padding: 0px;
            margin: 0px;
        """)
        header4.setAlignment(Qt.AlignLeft)
        header4.setFixedHeight(20)
        layout4.addWidget(header4)
        
        self.card_media_coleta.valor_label = QLabel("$0.00")
        self.card_media_coleta.valor_label.setStyleSheet("""
            font-size: 28px; 
            font-weight: bold; 
            color: #1F2937;
            background-color: transparent;
            border: none;
            padding: 0px;
            margin: 0px;
        """)
        self.card_media_coleta.valor_label.setAlignment(Qt.AlignLeft)
        self.card_media_coleta.valor_label.setFixedHeight(35)
        layout4.addWidget(self.card_media_coleta.valor_label)
        
        self.card_media_coleta.desc_label = QLabel("Média por coleta")
        self.card_media_coleta.desc_label.setStyleSheet("""
            font-size: 12px; 
            color: #6B7280;
            background-color: transparent;
            border: none;
            padding: 0px;
            margin: 0px;
        """)
        self.card_media_coleta.desc_label.setAlignment(Qt.AlignLeft)
        self.card_media_coleta.desc_label.setFixedHeight(15)
        layout4.addWidget(self.card_media_coleta.desc_label)
        
        layout4.addStretch()
        stats_layout.addWidget(self.card_media_coleta)

        # === CARD 5: TOTAL GERAL (TODAS AS POOLS) ===
        self.card_total_geral = QFrame()
        self.card_total_geral.setFixedSize(220, 140)
        self.card_total_geral.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 2px solid #8B5CF6;
                border-radius: 12px;
                padding: 0px;
                margin: 4px;
            }
        """)

        layout5 = QVBoxLayout(self.card_total_geral)
        layout5.setContentsMargins(16, 16, 16, 16)
        layout5.setSpacing(8)

        header5 = QLabel("Total Geral")
        header5.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            color: #8B5CF6;
            background-color: transparent;
            border: none;
            padding: 0px;
            margin: 0px;
        """)
        header5.setAlignment(Qt.AlignLeft)
        header5.setFixedHeight(20)
        layout5.addWidget(header5)

        self.card_total_geral.valor_label = QLabel("$0.00")
        self.card_total_geral.valor_label.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #1F2937;
            background-color: transparent;
            border: none;
            padding: 0px;
            margin: 0px;
        """)
        self.card_total_geral.valor_label.setAlignment(Qt.AlignLeft)
        self.card_total_geral.valor_label.setFixedHeight(35)
        layout5.addWidget(self.card_total_geral.valor_label)

        self.card_total_geral.desc_label = QLabel("Todas as pools")
        self.card_total_geral.desc_label.setStyleSheet("""
            font-size: 12px;
            color: #6B7280;
            background-color: transparent;
            border: none;
            padding: 0px;
            margin: 0px;
        """)
        self.card_total_geral.desc_label.setAlignment(Qt.AlignLeft)
        self.card_total_geral.desc_label.setFixedHeight(15)
        layout5.addWidget(self.card_total_geral.desc_label)

        layout5.addStretch()
        stats_layout.addWidget(self.card_total_geral)

        # Adicionar stretch no final para centralizar os cards
        stats_layout.addStretch()
        
        layout.addWidget(stats_frame)

    def forcar_atualizacao_visual(self):
        """Força atualização visual dos cards."""
        if hasattr(self, 'card_total_coletas'):
            self.card_total_coletas.repaint()
            self.card_total_coletas.update()
            
        if hasattr(self, 'card_total_acumulado'):
            self.card_total_acumulado.repaint()
            self.card_total_acumulado.update()
            
        if hasattr(self, 'card_taxa_acumulada'):
            self.card_taxa_acumulada.repaint() 
            self.card_taxa_acumulada.update()
            
        if hasattr(self, 'card_media_coleta'):
            self.card_media_coleta.repaint()
            self.card_media_coleta.update()

        if hasattr(self, 'card_total_geral'):
            self.card_total_geral.repaint()
            self.card_total_geral.update()


    def criar_secao_pools(self, layout):
        """Cria a seção de controle de pools em card."""
        pools_card = QFrame()
        pools_card.setStyleSheet(ModernStyles.get_card_style(True))
        
        pools_layout = QVBoxLayout(pools_card)
        pools_layout.setSpacing(16)
        
        # Título da seção
        titulo_layout = QHBoxLayout()
        titulo_label = QLabel("Gerenciamento de Pools")
        titulo_font = QFont()
        titulo_font.setPointSize(16)
        titulo_font.setBold(True)
        titulo_label.setFont(titulo_font)
        titulo_label.setStyleSheet("color: #1F2937; margin: 0;")
        titulo_layout.addWidget(titulo_label)
        titulo_layout.addStretch()
        pools_layout.addLayout(titulo_layout)
        
        # Controles
        controles_layout = QHBoxLayout()
        controles_layout.setSpacing(12)
        
        # Label e dropdown
        pool_label = QLabel("Pool Ativa:")
        pool_label.setStyleSheet("font-weight: 600; color: #374151; font-size: 14px;")
        controles_layout.addWidget(pool_label)
        
        self.combo_pools = QComboBox()
        self.combo_pools.setMinimumWidth(300)
        self.combo_pools.currentTextChanged.connect(self.pool_selecionada_mudou)
        self.combo_pools.setStyleSheet(ModernStyles.get_combo_style())
        controles_layout.addWidget(self.combo_pools)
        
        controles_layout.addStretch()
        
        # Botões modernos
        self.btn_nova_pool = QPushButton("Nova Pool")
        self.btn_nova_pool.setIcon(get_icon("plus"))
        self.btn_nova_pool.setIconSize(QSize(18, 18))
        self.btn_nova_pool.clicked.connect(self.nova_pool)
        self.btn_nova_pool.setStyleSheet(ModernStyles.get_button_style('success', 'medium'))
        controles_layout.addWidget(self.btn_nova_pool)

        self.btn_editar_pool = QPushButton("Editar")
        self.btn_editar_pool.setIcon(get_icon("edit"))
        self.btn_editar_pool.setIconSize(QSize(18, 18))
        self.btn_editar_pool.clicked.connect(self.editar_pool)
        self.btn_editar_pool.setStyleSheet(ModernStyles.get_button_style('primary', 'medium'))
        controles_layout.addWidget(self.btn_editar_pool)

        self.btn_excluir_pool = QPushButton("Excluir")
        self.btn_excluir_pool.setIcon(get_icon("trash"))
        self.btn_excluir_pool.setIconSize(QSize(18, 18))
        self.btn_excluir_pool.clicked.connect(self.excluir_pool)
        self.btn_excluir_pool.setStyleSheet(ModernStyles.get_button_style('danger', 'medium'))
        controles_layout.addWidget(self.btn_excluir_pool)
        
        pools_layout.addLayout(controles_layout)
        layout.addWidget(pools_card)
    
    def criar_secao_coletas(self, layout):
        """Cria a seção de controle de coletas em card."""
        coletas_card = QFrame()
        coletas_card.setStyleSheet(ModernStyles.get_card_style(True))
        
        coletas_layout = QVBoxLayout(coletas_card)
        coletas_layout.setSpacing(16)
        
        # Título da seção
        titulo_layout = QHBoxLayout()
        titulo_label = QLabel("Coletas da Pool Ativa")
        titulo_font = QFont()
        titulo_font.setPointSize(16)
        titulo_font.setBold(True)
        titulo_label.setFont(titulo_font)
        titulo_label.setStyleSheet("color: #1F2937; margin: 0;")
        titulo_layout.addWidget(titulo_label)
        titulo_layout.addStretch()
        coletas_layout.addLayout(titulo_layout)
        
        # Botões de ação
        acoes_layout = QHBoxLayout()
        acoes_layout.setSpacing(12)
        
        self.btn_nova_coleta = QPushButton("Nova Coleta")
        self.btn_nova_coleta.setIcon(get_icon("plus"))
        self.btn_nova_coleta.setIconSize(QSize(18, 18))
        self.btn_nova_coleta.clicked.connect(self.nova_coleta)
        self.btn_nova_coleta.setStyleSheet(ModernStyles.get_button_style('success', 'large'))
        acoes_layout.addWidget(self.btn_nova_coleta)

        acoes_layout.addStretch()

        self.btn_exportar = QPushButton("Exportar CSV")
        self.btn_exportar.setIcon(get_icon("chart"))
        self.btn_exportar.setIconSize(QSize(18, 18))
        self.btn_exportar.clicked.connect(self.exportar_dados)
        self.btn_exportar.setStyleSheet(ModernStyles.get_button_style('secondary', 'medium'))
        acoes_layout.addWidget(self.btn_exportar)

        self.btn_limpar = QPushButton("Limpar Dados")
        self.btn_limpar.setIcon(get_icon("trash"))
        self.btn_limpar.setIconSize(QSize(18, 18))
        self.btn_limpar.clicked.connect(self.limpar_dados)
        self.btn_limpar.setStyleSheet(ModernStyles.get_button_style('warning', 'medium'))
        acoes_layout.addWidget(self.btn_limpar)
        
        coletas_layout.addLayout(acoes_layout)
        layout.addWidget(coletas_card)
    
    def criar_tabela(self, layout):
        """Cria a tabela de dados moderna."""
        # Container para tabela
        table_card = QFrame()
        table_card.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #E5E7EB;
                border-radius: 12px;
                padding: 0px;
            }
        """)
        
        table_layout = QVBoxLayout(table_card)
        table_layout.setContentsMargins(0, 0, 0, 0)
        
        self.tabela = QTableWidget()
        self.tabela.setColumnCount(5)
        self.tabela.setHorizontalHeaderLabels(['Data', 'Dias', 'Valor (USD)', 'Taxa (%)', 'Acumulado (USD)'])
        
        # Configurar largura das colunas
        header = self.tabela.horizontalHeader()
        header.setStretchLastSection(True)
        self.tabela.setColumnWidth(0, 100)
        self.tabela.setColumnWidth(1, 70)
        self.tabela.setColumnWidth(2, 130)
        self.tabela.setColumnWidth(3, 100)
        
        # Habilitar seleção de linhas inteiras
        self.tabela.setSelectionBehavior(QTableWidget.SelectRows)
        
        # Habilitar menu contextual
        self.tabela.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tabela.customContextMenuRequested.connect(self.mostrar_menu_contextual)
        
        # Aplicar estilo moderno
        self.tabela.setStyleSheet(ModernStyles.get_table_style())
        
        table_layout.addWidget(self.tabela)
        layout.addWidget(table_card)
    
    def atualizar_combo_pools(self):
        """Atualiza o combo box com as pools disponíveis."""
        self.combo_pools.clear()
        self.combo_pools.blockSignals(True)

        pools = self.monitor.get_lista_pools()
        if not pools:
            self.combo_pools.addItem("Nenhuma pool configurada")
            self.combo_pools.setEnabled(False)
            self.combo_pools.blockSignals(False)
            return

        self.combo_pools.setEnabled(True)
        for pool in pools:
            self.combo_pools.addItem(pool.get_display_name(), pool.pool_id)

        # Selecionar pool ativa
        if self.monitor.pool_ativa_id:
            for i in range(self.combo_pools.count()):
                if self.combo_pools.itemData(i) == self.monitor.pool_ativa_id:
                    self.combo_pools.setCurrentIndex(i)
                    break

        self.combo_pools.blockSignals(False)
    
    def pool_selecionada_mudou(self):
        """Chamado quando a pool selecionada muda."""
        if self.combo_pools.currentData():
            self.monitor.definir_pool_ativa(self.combo_pools.currentData())
            self.atualizar_tabela()
            self.atualizar_cards_estatisticas()
    
    def atualizar_interface(self):
        """Atualiza toda a interface."""
        self.atualizar_combo_pools()
        self.atualizar_tabela()
        self.atualizar_cards_estatisticas()
        self.atualizar_botoes()
    
    def atualizar_botoes(self):
        """Atualiza o estado dos botões."""
        tem_pools = len(self.monitor.pools) > 0
        tem_pool_ativa = self.monitor.get_pool_ativa() is not None
        
        self.btn_editar_pool.setEnabled(tem_pool_ativa)
        self.btn_excluir_pool.setEnabled(tem_pools)
        self.btn_nova_coleta.setEnabled(tem_pool_ativa)
        self.btn_exportar.setEnabled(tem_pool_ativa)
        self.btn_limpar.setEnabled(tem_pool_ativa)
    
    def atualizar_tabela(self):
        """Atualiza a tabela com os dados da pool ativa."""
        dados = self.monitor.get_dados_pool_ativa()
        
        self.tabela.setRowCount(len(dados))
        
        total_acumulado = 0
        for i, coleta in enumerate(dados):
            total_acumulado += coleta.coleta_usd
            
            self.tabela.setItem(i, 0, QTableWidgetItem(coleta.data))
            self.tabela.setItem(i, 1, QTableWidgetItem(str(coleta.dias)))
            self.tabela.setItem(i, 2, QTableWidgetItem(f"${coleta.coleta_usd:.2f}"))
            self.tabela.setItem(i, 3, QTableWidgetItem(f"{coleta.taxa_percentual:.4f}%"))
            self.tabela.setItem(i, 4, QTableWidgetItem(f"${total_acumulado:.2f}"))
    
    def atualizar_cards_estatisticas(self):
        """Atualiza os cards de estatísticas com força de repaint."""
        
        try:
            dados = self.monitor.get_dados_pool_ativa()
            total_coletas = len(dados)
            total_acumulado = self.monitor.calcular_total_acumulado_pool_ativa()
            taxa_acumulada = self.monitor.calcular_taxa_acumulada_pool_ativa()
            
            # Calcular média por coleta
            media_coleta = total_acumulado / total_coletas if total_coletas > 0 else 0

            # Calculate total geral from all pools combined
            total_geral = self.monitor.calcular_total_acumulado_todas_pools()

            # Atualizar cards
            if hasattr(self, 'card_total_coletas') and hasattr(self.card_total_coletas, 'valor_label'):
                self.card_total_coletas.valor_label.setText(str(total_coletas))
                self.card_total_coletas.valor_label.repaint()  # ← FORÇAR REPAINT
                
            if hasattr(self, 'card_total_acumulado') and hasattr(self.card_total_acumulado, 'valor_label'):
                self.card_total_acumulado.valor_label.setText(f"${total_acumulado:.2f}")
                self.card_total_acumulado.valor_label.repaint()  # ← FORÇAR REPAINT
                
            if hasattr(self, 'card_taxa_acumulada') and hasattr(self.card_taxa_acumulada, 'valor_label'):
                self.card_taxa_acumulada.valor_label.setText(f"{taxa_acumulada:.2f}%")
                self.card_taxa_acumulada.valor_label.repaint()  # ← FORÇAR REPAINT
                
            if hasattr(self, 'card_media_coleta') and hasattr(self.card_media_coleta, 'valor_label'):
                self.card_media_coleta.valor_label.setText(f"${media_coleta:.2f}")
                self.card_media_coleta.valor_label.repaint()  # ← FORÇAR REPAINT

            if hasattr(self, 'card_total_geral') and hasattr(self.card_total_geral, 'valor_label'):
                self.card_total_geral.valor_label.setText(f"${total_geral:.2f}")
                self.card_total_geral.valor_label.repaint()

            # Forçar atualização visual geral
            self.forcar_atualizacao_visual()
            
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            import traceback
            traceback.print_exc()
    
    def nova_pool(self):
        """Abre diálogo para criar nova pool."""
        dialog = PoolConfigDialog(self, modo="criar")
        if dialog.exec() == QDialog.Accepted:
            dados = dialog.get_dados()
            try:
                pool_id = self.monitor.criar_nova_pool(
                    dados['nome'],
                    dados['data_abertura'],
                    dados['valor_inicial'],
                    dados['tipo_moeda']
                )
                self.monitor.definir_pool_ativa(pool_id)
                self.atualizar_interface()
                QMessageBox.information(self, "Sucesso", "Pool criada com sucesso!")
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao criar pool: {e}")
    
    def editar_pool(self):
        """Abre diálogo para editar pool ativa."""
        pool_config = self.monitor.get_pool_ativa()
        if not pool_config:
            QMessageBox.warning(self, "Aviso", "Nenhuma pool selecionada!")
            return
        
        dialog = PoolConfigDialog(self, pool_config, modo="editar")
        if dialog.exec() == QDialog.Accepted:
            dados = dialog.get_dados()
            try:
                self.monitor.atualizar_pool(
                    pool_config.pool_id,
                    dados['nome'],
                    dados['data_abertura'],
                    dados['valor_inicial'],
                    dados['tipo_moeda']
                )
                self.atualizar_interface()
                QMessageBox.information(self, "Sucesso", "Pool atualizada com sucesso!")
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao atualizar pool: {e}")
    
    def excluir_pool(self):
        """Abre diálogo para excluir pool."""
        pools = self.monitor.get_lista_pools()
        if not pools:
            QMessageBox.warning(self, "Aviso", "Nenhuma pool disponível para exclusão!")
            return
        
        dialog = SelecionarPoolDialog(self, pools)
        if dialog.exec() == QDialog.Accepted:
            pool_id = dialog.get_pool_selecionada()
            if pool_id:
                try:
                    self.monitor.excluir_pool(pool_id)
                    self.atualizar_interface()
                    QMessageBox.information(self, "Sucesso", "Pool excluída com sucesso!")
                except Exception as e:
                    QMessageBox.critical(self, "Erro", f"Erro ao excluir pool: {e}")
    
    def nova_coleta(self):
        """Abre diálogo para nova coleta."""
        if not self.monitor.get_pool_ativa():
            QMessageBox.warning(self, "Aviso", "Configure uma pool antes de registrar coletas!")
            return
        
        dialog = NovaColetaDialog(self)
        if dialog.exec() == QDialog.Accepted:
            dados = dialog.get_dados()
            try:
                self.monitor.registrar_nova_coleta(dados['data'], dados['valor'])
                self.atualizar_tabela()
                self.atualizar_cards_estatisticas()
                QMessageBox.information(self, "Sucesso", "Coleta registrada com sucesso!")
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao registrar coleta: {e}")
    
    def exportar_dados(self):
        """Exporta dados para CSV."""
        if not self.monitor.get_pool_ativa():
            QMessageBox.warning(self, "Aviso", "Nenhuma pool ativa para exportar!")
            return
        
        pool_config = self.monitor.get_pool_ativa()
        nome_sugerido = f"coletas_{pool_config.nome.replace(' ', '_')}.csv"
        
        arquivo, _ = QFileDialog.getSaveFileName(
            self,
            "Exportar Dados",
            nome_sugerido,
            "Arquivos CSV (*.csv)"
        )
        
        if arquivo:
            try:
                self.monitor.exportar_dados_pool_ativa(arquivo)
                QMessageBox.information(self, "Sucesso", f"Dados exportados para: {arquivo}")
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao exportar dados: {e}")
    
    def limpar_dados(self):
        """Limpa todos os dados da pool ativa."""
        if not self.monitor.get_pool_ativa():
            QMessageBox.warning(self, "Aviso", "Nenhuma pool ativa!")
            return
        
        pool_config = self.monitor.get_pool_ativa()
        resposta = QMessageBox.question(
            self,
            "Confirmar Limpeza",
            f"Tem certeza que deseja limpar todos os dados da pool '{pool_config.nome}'?\\n\\nEsta ação não pode ser desfeita!",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if resposta == QMessageBox.Yes:
            try:
                self.monitor.limpar_dados_pool_ativa()
                self.atualizar_tabela()
                self.atualizar_cards_estatisticas()
                QMessageBox.information(self, "Sucesso", "Dados limpos com sucesso!")
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao limpar dados: {e}")
    
    def mostrar_menu_contextual(self, position):
        """Mostra menu contextual ao clicar com botão direito na tabela."""
        if not self.tabela.itemAt(position):
            return
        
        linha_selecionada = self.tabela.rowAt(position.y())
        if linha_selecionada < 0:
            return
        
        # Criar menu contextual
        menu = QMenu(self)
        
        # Ação editar coleta
        acao_editar = QAction("Editar Coleta", self)
        acao_editar.setIcon(get_icon("edit"))
        acao_editar.triggered.connect(lambda: self.editar_coleta(linha_selecionada))
        menu.addAction(acao_editar)

        # Separador
        menu.addSeparator()

        # Ação excluir coleta
        acao_excluir = QAction("Excluir Coleta", self)
        acao_excluir.setIcon(get_icon("trash"))
        acao_excluir.triggered.connect(lambda: self.excluir_coleta(linha_selecionada))
        menu.addAction(acao_excluir)
        
        # Mostrar menu na posição do cursor
        menu.exec(self.tabela.mapToGlobal(position))
    
    def editar_coleta(self, linha_index):
        """Edita uma coleta específica."""
        dados = self.monitor.get_dados_pool_ativa()
        if linha_index >= len(dados):
            return
        
        coleta = dados[linha_index]
        
        # Usar o mesmo diálogo de nova coleta, mas preenchido
        dialog = EditarColetaDialog(self, coleta)
        if dialog.exec() == QDialog.Accepted:
            novos_dados = dialog.get_dados()
            try:
                # Atualizar a coleta
                self.monitor.atualizar_coleta(linha_index, novos_dados['data'], novos_dados['valor'])
                self.atualizar_tabela()
                self.atualizar_cards_estatisticas()
                QMessageBox.information(self, "Sucesso", "Coleta atualizada com sucesso!")
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao atualizar coleta: {e}")
    
    def excluir_coleta(self, linha_index):
        """Exclui uma coleta específica."""
        dados = self.monitor.get_dados_pool_ativa()
        if linha_index >= len(dados):
            return
        
        coleta = dados[linha_index]
        
        # Confirmar exclusão
        resposta = QMessageBox.question(
            self,
            "Confirmar Exclusão",
            f"Tem certeza que deseja excluir a coleta do dia {coleta.data}?\\n\\nValor: ${coleta.coleta_usd:.2f}\\nEsta ação não pode ser desfeita!",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if resposta == QMessageBox.Yes:
            try:
                self.monitor.excluir_coleta(linha_index)
                self.atualizar_tabela()
                self.atualizar_cards_estatisticas()
                QMessageBox.information(self, "Sucesso", "Coleta excluída com sucesso!")
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao excluir coleta: {e}")
    
    # === MÉTODOS OPCIONAIS PARA SALVAR/RESTAURAR TAMANHO ===
    # Descomente se quiser que a janela lembre do tamanho:
    
    def restore_window_state(self):
        """Restaura o tamanho e posição salvos da janela."""
        try:
            from PySide6.QtCore import QSettings
            settings = QSettings("MonitorColetas", "WindowState")
            
            # Restaurar geometria
            geometry = settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
            
            # Restaurar estado (maximizada, etc.)
            state = settings.value("windowState")
            if state:
                self.restoreState(state)
                
        except Exception as e:
            print(f"Erro ao restaurar estado da janela: {e}")

    def save_window_state(self):
        """Salva o tamanho e posição atual da janela."""
        try:
            from PySide6.QtCore import QSettings
            settings = QSettings("MonitorColetas", "WindowState")
            
            # Salvar geometria
            settings.setValue("geometry", self.saveGeometry())
            
            # Salvar estado
            settings.setValue("windowState", self.saveState())
            
        except Exception as e:
            print(f"Erro ao salvar estado da janela: {e}")

    def closeEvent(self, event):
        """Chamado quando a janela vai fechar."""
        # Salvar estado da janela antes de fechar (descomente para ativar)
        # self.save_window_state()
        event.accept()