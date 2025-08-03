import sys
from datetime import datetime
from PySide6.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, 
                               QPushButton, QTableWidget, QTableWidgetItem, 
                               QLineEdit, QLabel, QDateEdit, QMessageBox,
                               QGroupBox, QFormLayout, QHeaderView)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QFont

from core.monitor import MonitorLiquidez
from gui.dialogs import PoolConfigDialog


class MonitorColetasApp(QMainWindow):
    """Janela principal do Monitor de Coletas."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Monitor de Coletas - Pool de Liquidez")
        self.setGeometry(100, 100, 1000, 700)
        
        # Inicializar monitor de liquidez
        self.monitor = MonitorLiquidez()
        
        # Setup da interface
        self.setup_ui()
        
        # Carregar dados existentes na tabela
        self.carregar_dados_tabela()
    
    def setup_ui(self):
        """Configura a interface principal."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Título
        title = QLabel("Monitor de Coletas - Pool de Liquidez")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)
        
        # Seção de configuração da pool
        self.setup_config_section(main_layout)
        
        # Seção de nova coleta
        self.setup_nova_coleta_section(main_layout)
        
        # Tabela de coletas
        self.setup_tabela(main_layout)
        
        # Botões de ação
        self.setup_botoes(main_layout)
    
    def setup_config_section(self, main_layout):
        """Configura a seção de configuração da pool."""
        config_group = QGroupBox("Configuração da Pool")
        config_layout = QHBoxLayout()
        
        # Labels de informação
        self.info_pool = QLabel("Pool não configurada")
        self.info_pool.setStyleSheet("color: red; font-weight: bold;")
        config_layout.addWidget(self.info_pool)
        
        config_layout.addStretch()
        
        # Botão para configurar/editar pool
        self.btn_config_pool = QPushButton("Configurar Pool")
        self.btn_config_pool.clicked.connect(self.configurar_pool)
        config_layout.addWidget(self.btn_config_pool)
        
        config_group.setLayout(config_layout)
        main_layout.addWidget(config_group)
        
        # Atualizar display da configuração
        self.atualizar_info_pool()
    
    def setup_nova_coleta_section(self, main_layout):
        """Configura a seção de nova coleta."""
        coleta_group = QGroupBox("Nova Coleta")
        coleta_layout = QFormLayout()
        
        # Data da coleta
        self.data_coleta = QDateEdit()
        self.data_coleta.setDate(QDate.currentDate())
        self.data_coleta.setCalendarPopup(True)
        coleta_layout.addRow("Data da Coleta:", self.data_coleta)
        
        # Valor coletado
        self.valor_coleta = QLineEdit()
        self.valor_coleta.setPlaceholderText("Ex: 25.75")
        coleta_layout.addRow("Valor Coletado (USD):", self.valor_coleta)
        
        # Botão adicionar
        self.btn_adicionar = QPushButton("Adicionar Coleta")
        self.btn_adicionar.clicked.connect(self.adicionar_coleta)
        coleta_layout.addRow("", self.btn_adicionar)
        
        coleta_group.setLayout(coleta_layout)
        main_layout.addWidget(coleta_group)
    
    def setup_tabela(self, main_layout):
        """Configura a tabela de coletas."""
        # Label da tabela
        tabela_label = QLabel("Histórico de Coletas")
        tabela_label.setFont(QFont("Arial", 12, QFont.Bold))
        main_layout.addWidget(tabela_label)
        
        # Tabela
        self.tabela = QTableWidget()
        self.tabela.setColumnCount(4)
        self.tabela.setHorizontalHeaderLabels([
            "Data da Coleta", "Valor Coletado (USD)", "Taxa (%)", "Acumulado (USD)"
        ])
        
        # Configurar header da tabela
        header = self.tabela.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        
        main_layout.addWidget(self.tabela)
    
    def setup_botoes(self, main_layout):
        """Configura os botões de ação."""
        botoes_layout = QHBoxLayout()
        
        # Botão exportar
        btn_exportar = QPushButton("Exportar CSV")
        btn_exportar.clicked.connect(self.exportar_dados)
        botoes_layout.addWidget(btn_exportar)
        
        # Botão limpar dados
        btn_limpar = QPushButton("Limpar Dados")
        btn_limpar.clicked.connect(self.limpar_dados)
        botoes_layout.addWidget(btn_limpar)
        
        botoes_layout.addStretch()
        
        # Botão sair
        btn_sair = QPushButton("Sair")
        btn_sair.clicked.connect(self.close)
        botoes_layout.addWidget(btn_sair)
        
        main_layout.addLayout(botoes_layout)
    
    def configurar_pool(self):
        """Abre diálogo para configurar a pool."""
        dialog = PoolConfigDialog(self, self.monitor.pool_config)
        
        if dialog.exec() == PoolConfigDialog.Accepted:
            try:
                config = dialog.get_config()
                self.monitor.salvar_config_pool(config)
                self.atualizar_info_pool()
                self.monitor.recalcular_taxas()
                self.carregar_dados_tabela()
                QMessageBox.information(self, "Sucesso", "Configuração da pool salva com sucesso!")
            except ValueError:
                QMessageBox.warning(self, "Erro", "Por favor, insira um valor inicial válido.")
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao salvar configuração: {e}")
    
    def atualizar_info_pool(self):
        """Atualiza as informações da pool na interface."""
        if self.monitor.pool_config:
            config = self.monitor.pool_config
            info_text = f"Pool: {config.tipo_moeda} | "
            info_text += f"Abertura: {config.data_abertura} | "
            info_text += f"Valor Inicial: ${config.valor_inicial:.2f}"
            self.info_pool.setText(info_text)
            self.info_pool.setStyleSheet("color: green; font-weight: bold;")
            self.btn_config_pool.setText("Editar Pool")
        else:
            self.info_pool.setText("Pool não configurada")
            self.info_pool.setStyleSheet("color: red; font-weight: bold;")
            self.btn_config_pool.setText("Configurar Pool")
    
    def adicionar_coleta(self):
        """Adiciona uma nova coleta."""
        if not self.monitor.pool_config:
            QMessageBox.warning(self, "Erro", "Configure a pool antes de adicionar coletas.")
            return
        
        try:
            data = self.data_coleta.date().toString("yyyy-MM-dd")
            valor = float(self.valor_coleta.text())
            
            # Registrar coleta
            self.monitor.registrar_nova_coleta(data, valor)
            
            # Atualizar tabela
            self.carregar_dados_tabela()
            
            # Limpar campos
            self.valor_coleta.clear()
            self.data_coleta.setDate(QDate.currentDate())
            
            QMessageBox.information(self, "Sucesso", "Coleta adicionada com sucesso!")
            
        except ValueError:
            QMessageBox.warning(self, "Erro", "Por favor, insira um valor válido.")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao adicionar coleta: {e}")
    
    def carregar_dados_tabela(self):
        """Carrega os dados do monitor na tabela."""
        self.tabela.setRowCount(0)
        
        total_acumulado = 0
        for i, coleta in enumerate(self.monitor.dados):
            self.tabela.insertRow(i)
            total_acumulado += coleta.coleta_usd
            
            self.tabela.setItem(i, 0, QTableWidgetItem(coleta.data))
            self.tabela.setItem(i, 1, QTableWidgetItem(f"{coleta.coleta_usd:.2f}"))
            self.tabela.setItem(i, 2, QTableWidgetItem(f"{coleta.taxa_percentual:.4f}"))
            self.tabela.setItem(i, 3, QTableWidgetItem(f"{total_acumulado:.2f}"))
    
    def exportar_dados(self):
        """Exporta os dados para um arquivo CSV."""
        if not self.monitor.dados:
            QMessageBox.information(self, "Info", "Não há dados para exportar.")
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"coletas_export_{timestamp}.csv"
        
        try:
            self.monitor.exportar_dados(filename)
            QMessageBox.information(self, "Sucesso", f"Dados exportados para {filename}")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao exportar dados: {e}")
    
    def limpar_dados(self):
        """Limpa todos os dados de coletas."""
        reply = QMessageBox.question(
            self, "Confirmar", 
            "Tem certeza que deseja limpar todos os dados de coletas?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                self.monitor.limpar_dados()
                self.carregar_dados_tabela()
                QMessageBox.information(self, "Sucesso", "Dados limpos com sucesso!")
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao limpar dados: {e}")