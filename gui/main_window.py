import sys
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                               QPushButton, QTableWidget, QTableWidgetItem, QLabel,
                               QMessageBox, QFileDialog, QComboBox, QFrame, QDialog,
                               QMenuBar, QMenu)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QIcon, QPalette, QAction

from core.monitor import MonitorLiquidez
from gui.dialogs import PoolConfigDialog, NovaColetaDialog, SelecionarPoolDialog
from gui.about_dialog import AboutDialog

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
        <h3>⌨️ Atalhos de Teclado</h3>
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
        """Configura a interface principal."""
        self.setWindowTitle("Monitor de Coletas - Pools de Liquidez")
        self.setGeometry(100, 100, 900, 600)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Cabeçalho
        self.criar_cabecalho(layout)
        
        # Seção de controle de pools
        self.criar_secao_pools(layout)
        
        # Separador
        separador = QFrame()
        separador.setFrameShape(QFrame.HLine)
        separador.setFrameShadow(QFrame.Sunken)
        layout.addWidget(separador)
        
        # Seção de coletas
        self.criar_secao_coletas(layout)
        
        # Tabela de dados
        self.criar_tabela(layout)
        
        # Rodapé com totais
        self.criar_rodape(layout)
    
    def criar_cabecalho(self, layout):
        """Cria o cabeçalho da aplicação."""
        titulo_label = QLabel("🏊‍♂️ Monitor de Coletas - Pools de Liquidez")
        titulo_font = QFont()
        titulo_font.setPointSize(18)
        titulo_font.setBold(True)
        titulo_label.setFont(titulo_font)
        titulo_label.setAlignment(Qt.AlignCenter)
        cor = self.palette().color(QPalette.WindowText).name()
        titulo_label.setStyleSheet(f"color: {cor}; margin: 10px 0;")
        layout.addWidget(titulo_label)
    
    def criar_secao_pools(self, layout):
        """Cria a seção de controle de pools."""
        # Label da seção
        secao_label = QLabel("🏊 Gerenciamento de Pools")
        secao_font = QFont()
        secao_font.setPointSize(12)
        secao_font.setBold(True)
        secao_label.setFont(secao_font)
        cor = self.palette().color(QPalette.WindowText).name()
        secao_label.setStyleSheet(f"color: {cor}; margin: 10px 0;")
        layout.addWidget(secao_label)
        
        # Layout horizontal para controles de pool
        pools_layout = QHBoxLayout()
        
        # Dropdown de seleção de pool
        pool_label = QLabel("Pool Ativa:")
        pools_layout.addWidget(pool_label)
        
        self.combo_pools = QComboBox()
        self.combo_pools.setMinimumWidth(300)
        self.combo_pools.currentTextChanged.connect(self.pool_selecionada_mudou)
        pools_layout.addWidget(self.combo_pools)
        
        pools_layout.addStretch()
        
        # Botões de gerenciamento
        self.btn_nova_pool = QPushButton("➕ Nova Pool")
        self.btn_nova_pool.clicked.connect(self.nova_pool)
        self.btn_nova_pool.setStyleSheet("background-color: #27ae60; color: white; padding: 8px 15px; border-radius: 5px;")
        pools_layout.addWidget(self.btn_nova_pool)
        
        self.btn_editar_pool = QPushButton("✏️ Editar")
        self.btn_editar_pool.clicked.connect(self.editar_pool)
        self.btn_editar_pool.setStyleSheet("background-color: #3498db; color: white; padding: 8px 15px; border-radius: 5px;")
        pools_layout.addWidget(self.btn_editar_pool)
        
        self.btn_excluir_pool = QPushButton("🗑️ Excluir")
        self.btn_excluir_pool.clicked.connect(self.excluir_pool)
        self.btn_excluir_pool.setStyleSheet("background-color: #e74c3c; color: white; padding: 8px 15px; border-radius: 5px;")
        pools_layout.addWidget(self.btn_excluir_pool)
        
        layout.addLayout(pools_layout)
    
    def criar_secao_coletas(self, layout):
        """Cria a seção de controle de coletas."""
        # Label da seção
        secao_label = QLabel("💰 Coletas da Pool Ativa")
        secao_font = QFont()
        secao_font.setPointSize(12)
        secao_font.setBold(True)
        secao_label.setFont(secao_font)
        cor = self.palette().color(QPalette.WindowText).name()
        secao_label.setStyleSheet(f"color: {cor}; margin: 10px 0;")
        layout.addWidget(secao_label)
        
        # Layout horizontal para botões de coleta
        coletas_layout = QHBoxLayout()
        
        self.btn_nova_coleta = QPushButton("➕ Nova Coleta")
        self.btn_nova_coleta.clicked.connect(self.nova_coleta)
        self.btn_nova_coleta.setStyleSheet("background-color: #27ae60; color: white; padding: 10px 20px; border-radius: 5px; font-weight: bold;")
        coletas_layout.addWidget(self.btn_nova_coleta)
        
        coletas_layout.addStretch()
        
        self.btn_exportar = QPushButton("📊 Exportar CSV")
        self.btn_exportar.clicked.connect(self.exportar_dados)
        self.btn_exportar.setStyleSheet("background-color: #9b59b6; color: white; padding: 10px 20px; border-radius: 5px;")
        coletas_layout.addWidget(self.btn_exportar)
        
        self.btn_limpar = QPushButton("🗑️ Limpar Dados")
        self.btn_limpar.clicked.connect(self.limpar_dados)
        self.btn_limpar.setStyleSheet("background-color: #e67e22; color: white; padding: 10px 20px; border-radius: 5px;")
        coletas_layout.addWidget(self.btn_limpar)
        
        layout.addLayout(coletas_layout)
    
    def criar_tabela(self, layout):
        """Cria a tabela de dados."""
        self.tabela = QTableWidget()
        self.tabela.setColumnCount(4)
        self.tabela.setHorizontalHeaderLabels(['Data', 'Valor (USD)', 'Taxa (%)', 'Acumulado (USD)'])
        
        # Configurar largura das colunas
        header = self.tabela.horizontalHeader()
        header.setStretchLastSection(True)
        self.tabela.setColumnWidth(0, 120)
        self.tabela.setColumnWidth(1, 150)
        self.tabela.setColumnWidth(2, 120)
        
        # Estilo da tabela
        self.tabela.setAlternatingRowColors(True)
        self.tabela.setStyleSheet("""
            QTableWidget {
                gridline-color: #bdc3c7;
                background-color: white;
                alternate-background-color: #ecf0f1;
                color: #2c3e50;
            }
            QHeaderView::section {
                background-color: #34495e;
                color: white;
                padding: 10px;
                font-weight: bold;
            }
        """)
        
        layout.addWidget(self.tabela)
    
    def criar_rodape(self, layout):
        """Cria o rodapé com informações de totais."""
        rodape_layout = QHBoxLayout()
        
        self.label_total_coletas = QLabel("Total de Coletas: 0")
        self.label_total_coletas.setStyleSheet("font-weight: bold; color: #2c3e50;")
        rodape_layout.addWidget(self.label_total_coletas)
        
        rodape_layout.addStretch()
        
        self.label_total_acumulado = QLabel("Total Acumulado: $0.00")
        self.label_total_acumulado.setStyleSheet("font-weight: bold; color: #27ae60; font-size: 14px;")
        rodape_layout.addWidget(self.label_total_acumulado)
        
        rodape_layout.addStretch()
        
        self.label_taxa_acumulada = QLabel("Taxa Acumulada: 0.00%")
        self.label_taxa_acumulada.setStyleSheet("font-weight: bold; color: #e74c3c; font-size: 14px;")
        rodape_layout.addWidget(self.label_taxa_acumulada)
        
        layout.addLayout(rodape_layout)
    
    def atualizar_combo_pools(self):
        """Atualiza o combo box com as pools disponíveis."""
        self.combo_pools.clear()
        
        pools = self.monitor.get_lista_pools()
        if not pools:
            self.combo_pools.addItem("Nenhuma pool configurada")
            self.combo_pools.setEnabled(False)
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
    
    def pool_selecionada_mudou(self):
        """Chamado quando a pool selecionada muda."""
        if self.combo_pools.currentData():
            self.monitor.definir_pool_ativa(self.combo_pools.currentData())
            self.atualizar_tabela()
            self.atualizar_totais()
    
    def atualizar_interface(self):
        """Atualiza toda a interface."""
        self.atualizar_combo_pools()
        self.atualizar_tabela()
        self.atualizar_totais()
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
            self.tabela.setItem(i, 1, QTableWidgetItem(f"${coleta.coleta_usd:.2f}"))
            self.tabela.setItem(i, 2, QTableWidgetItem(f"{coleta.taxa_percentual:.4f}%"))
            self.tabela.setItem(i, 3, QTableWidgetItem(f"${total_acumulado:.2f}"))
    
    def atualizar_totais(self):
        """Atualiza os labels de totais."""
        dados = self.monitor.get_dados_pool_ativa()
        total_coletas = len(dados)
        total_acumulado = self.monitor.calcular_total_acumulado_pool_ativa()
        taxa_acumulada = self.monitor.calcular_taxa_acumulada_pool_ativa()
        
        self.label_total_coletas.setText(f"Total de Coletas: {total_coletas}")
        self.label_total_acumulado.setText(f"Total Acumulado: ${total_acumulado:.2f}")
        self.label_taxa_acumulada.setText(f"Taxa Acumulada: {taxa_acumulada:.4f}%")
    
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
                self.atualizar_totais()
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
                self.atualizar_totais()
                QMessageBox.information(self, "Sucesso", "Dados limpos com sucesso!")
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao limpar dados: {e}")