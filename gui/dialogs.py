# 3. gui/dialogs.py - Atualizado para múltiplas pools
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
                                     QLineEdit, QDoubleSpinBox, QDateEdit, QPushButton,
                                     QMessageBox, QLabel, QComboBox)
from PySide6.QtCore import QDate, Qt
from PySide6.QtGui import QFont

from models.pool_config import PoolConfig

class PoolConfigDialog(QDialog):
    """Diálogo para criar/editar configuração de pool."""
    
    def __init__(self, parent=None, pool_config=None, modo="criar"):
        super().__init__(parent)
        self.pool_config = pool_config
        self.modo = modo  # "criar" ou "editar"
        self.setup_ui()
        
        if pool_config and modo == "editar":
            self.carregar_dados_pool()
    
    def setup_ui(self):
        """Configura a interface do diálogo."""
        titulo = "Nova Pool" if self.modo == "criar" else "Editar Pool"
        self.setWindowTitle(titulo)
        self.setModal(True)
        self.resize(400, 300)
        
        # Layout principal
        layout = QVBoxLayout(self)
        
        # Título
        titulo_label = QLabel(titulo)
        titulo_font = QFont()
        titulo_font.setPointSize(14)
        titulo_font.setBold(True)
        titulo_label.setFont(titulo_font)
        titulo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo_label)
        
        # Formulário
        form_layout = QFormLayout()
        
        # Nome da Pool
        self.nome_edit = QLineEdit()
        self.nome_edit.setPlaceholderText("Ex: Pool Principal, Pool Secundária...")
        form_layout.addRow("Nome da Pool:", self.nome_edit)
        
        # Tipo de Moeda
        self.tipo_moeda_edit = QLineEdit()
        self.tipo_moeda_edit.setPlaceholderText("Ex: USDC/ETH, DAI/USDC, WBTC/ETH...")
        form_layout.addRow("Par de Moedas:", self.tipo_moeda_edit)
        
        # Data de Abertura
        self.data_abertura_edit = QDateEdit()
        self.data_abertura_edit.setDate(QDate.currentDate())
        self.data_abertura_edit.setCalendarPopup(True)
        form_layout.addRow("Data de Abertura:", self.data_abertura_edit)
        
        # Valor Inicial
        self.valor_inicial_edit = QDoubleSpinBox()
        self.valor_inicial_edit.setRange(0.01, 999999999.99)
        self.valor_inicial_edit.setDecimals(2)
        self.valor_inicial_edit.setSuffix(" USD")
        self.valor_inicial_edit.setValue(1000.00)
        form_layout.addRow("Valor Inicial:", self.valor_inicial_edit)
        
        layout.addLayout(form_layout)
        
        # Botões
        botoes_layout = QHBoxLayout()
        
        self.btn_cancelar = QPushButton("Cancelar")
        self.btn_cancelar.clicked.connect(self.reject)
        
        texto_confirmar = "Criar Pool" if self.modo == "criar" else "Salvar Alterações"
        self.btn_confirmar = QPushButton(texto_confirmar)
        self.btn_confirmar.clicked.connect(self.confirmar)
        self.btn_confirmar.setDefault(True)
        
        botoes_layout.addWidget(self.btn_cancelar)
        botoes_layout.addWidget(self.btn_confirmar)
        
        layout.addLayout(botoes_layout)
    
    def carregar_dados_pool(self):
        """Carrega dados da pool para edição."""
        if self.pool_config:
            self.nome_edit.setText(self.pool_config.nome)
            self.tipo_moeda_edit.setText(self.pool_config.tipo_moeda)
            self.valor_inicial_edit.setValue(self.pool_config.valor_inicial)
            
            # Converter data string para QDate
            try:
                data_parts = self.pool_config.data_abertura.split('/')
                if len(data_parts) == 3:
                    dia, mes, ano = map(int, data_parts)
                    self.data_abertura_edit.setDate(QDate(ano, mes, dia))
            except:
                self.data_abertura_edit.setDate(QDate.currentDate())
    
    def confirmar(self):
        """Valida e confirma os dados."""
        # Validações
        if not self.nome_edit.text().strip():
            QMessageBox.warning(self, "Erro", "Nome da pool é obrigatório!")
            return
        
        if not self.tipo_moeda_edit.text().strip():
            QMessageBox.warning(self, "Erro", "Par de moedas é obrigatório!")
            return
        
        if self.valor_inicial_edit.value() <= 0:
            QMessageBox.warning(self, "Erro", "Valor inicial deve ser maior que zero!")
            return
        
        self.accept()
    
    def get_dados(self):
        """Retorna os dados preenchidos."""
        data_abertura = self.data_abertura_edit.date().toString("dd/MM/yyyy")
        
        return {
            'nome': self.nome_edit.text().strip(),
            'tipo_moeda': self.tipo_moeda_edit.text().strip(),
            'data_abertura': data_abertura,
            'valor_inicial': self.valor_inicial_edit.value()
        }


class NovaColetaDialog(QDialog):
    """Diálogo para registrar nova coleta."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """Configura a interface do diálogo."""
        self.setWindowTitle("Nova Coleta")
        self.setModal(True)
        self.resize(350, 200)
        
        # Layout principal
        layout = QVBoxLayout(self)
        
        # Título
        titulo_label = QLabel("Registrar Nova Coleta")
        titulo_font = QFont()
        titulo_font.setPointSize(14)
        titulo_font.setBold(True)
        titulo_label.setFont(titulo_font)
        titulo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo_label)
        
        # Formulário
        form_layout = QFormLayout()
        
        # Data da Coleta
        self.data_coleta_edit = QDateEdit()
        self.data_coleta_edit.setDate(QDate.currentDate())
        self.data_coleta_edit.setCalendarPopup(True)
        form_layout.addRow("Data da Coleta:", self.data_coleta_edit)
        
        # Valor Coletado
        self.valor_coleta_edit = QDoubleSpinBox()
        self.valor_coleta_edit.setRange(0.01, 999999999.99)
        self.valor_coleta_edit.setDecimals(2)
        self.valor_coleta_edit.setSuffix(" USD")
        self.valor_coleta_edit.setValue(100.00)
        form_layout.addRow("Valor Coletado:", self.valor_coleta_edit)
        
        layout.addLayout(form_layout)
        
        # Botões
        botoes_layout = QHBoxLayout()
        
        self.btn_cancelar = QPushButton("Cancelar")
        self.btn_cancelar.clicked.connect(self.reject)
        
        self.btn_confirmar = QPushButton("Registrar Coleta")
        self.btn_confirmar.clicked.connect(self.confirmar)
        self.btn_confirmar.setDefault(True)
        
        botoes_layout.addWidget(self.btn_cancelar)
        botoes_layout.addWidget(self.btn_confirmar)
        
        layout.addLayout(botoes_layout)
    
    def confirmar(self):
        """Valida e confirma os dados."""
        if self.valor_coleta_edit.value() <= 0:
            QMessageBox.warning(self, "Erro", "Valor da coleta deve ser maior que zero!")
            return
        
        self.accept()
    
    def get_dados(self):
        """Retorna os dados preenchidos."""
        data_coleta = self.data_coleta_edit.date().toString("dd/MM/yyyy")
        
        return {
            'data': data_coleta,
            'valor': self.valor_coleta_edit.value()
        }


class SelecionarPoolDialog(QDialog):
    """Diálogo para selecionar pool para exclusão."""
    
    def __init__(self, parent=None, pools=None):
        super().__init__(parent)
        self.pools = pools or []
        self.pool_selecionada = None
        self.setup_ui()
    
    def setup_ui(self):
        """Configura a interface do diálogo."""
        self.setWindowTitle("Selecionar Pool")
        self.setModal(True)
        self.resize(400, 200)
        
        # Layout principal
        layout = QVBoxLayout(self)
        
        # Título
        titulo_label = QLabel("Selecione a pool para excluir:")
        titulo_font = QFont()
        titulo_font.setPointSize(12)
        titulo_font.setBold(True)
        titulo_label.setFont(titulo_font)
        layout.addWidget(titulo_label)
        
        # ComboBox com pools
        self.combo_pools = QComboBox()
        for pool in self.pools:
            self.combo_pools.addItem(pool.get_display_name(), pool.pool_id)
        
        layout.addWidget(self.combo_pools)
        
        # Aviso
        aviso_label = QLabel("⚠️ Esta ação não pode ser desfeita!")
        aviso_label.setStyleSheet("color: red; font-weight: bold;")
        layout.addWidget(aviso_label)
        
        # Botões
        botoes_layout = QHBoxLayout()
        
        self.btn_cancelar = QPushButton("Cancelar")
        self.btn_cancelar.clicked.connect(self.reject)
        
        self.btn_excluir = QPushButton("Excluir Pool")
        self.btn_excluir.clicked.connect(self.confirmar_exclusao)
        self.btn_excluir.setStyleSheet("background-color: #dc3545; color: white;")
        
        botoes_layout.addWidget(self.btn_cancelar)
        botoes_layout.addWidget(self.btn_excluir)
        
        layout.addLayout(botoes_layout)
    
    def confirmar_exclusao(self):
        """Confirma a exclusão da pool."""
        if self.combo_pools.currentIndex() < 0:
            QMessageBox.warning(self, "Erro", "Selecione uma pool para excluir!")
            return
        
        pool_nome = self.combo_pools.currentText()
        resposta = QMessageBox.question(
            self, 
            "Confirmar Exclusão",
            f"Tem certeza que deseja excluir a pool '{pool_nome}'?\\n\\nTodos os dados serão perdidos permanentemente!",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if resposta == QMessageBox.Yes:
            self.pool_selecionada = self.combo_pools.currentData()
            self.accept()
    
    def get_pool_selecionada(self):
        """Retorna o ID da pool selecionada."""
        return self.pool_selecionada
