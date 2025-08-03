from PySide6.QtWidgets import (QDialog, QVBoxLayout, QFormLayout, QDateEdit, 
                               QLineEdit, QComboBox, QDialogButtonBox)
from PySide6.QtCore import QDate

from models.pool_config import PoolConfig


class PoolConfigDialog(QDialog):
    """Diálogo para configuração da pool de liquidez."""
    
    def __init__(self, parent=None, config=None):
        super().__init__(parent)
        self.setWindowTitle("Configuração da Pool")
        self.setModal(True)
        self.resize(400, 300)
        
        self.setup_ui()
        
        # Se há configuração existente, preencher campos
        if config:
            self.load_config(config)
    
    def setup_ui(self):
        """Configura a interface do diálogo."""
        layout = QVBoxLayout()
        
        # Form layout
        form_layout = QFormLayout()
        
        # Data de abertura da pool
        self.data_abertura = QDateEdit()
        self.data_abertura.setDate(QDate.currentDate())
        self.data_abertura.setCalendarPopup(True)
        form_layout.addRow("Data de Abertura:", self.data_abertura)
        
        # Valor inicial da pool
        self.valor_inicial = QLineEdit()
        self.valor_inicial.setPlaceholderText("Ex: 1000.50")
        form_layout.addRow("Valor Inicial (USD):", self.valor_inicial)
        
        # Tipo de moeda
        self.tipo_moeda = QComboBox()
        self.tipo_moeda.addItems([
            "ETH/USDC", "BTC/ETH", "BTC/USDC", "WETH/USDC", "Outro"
        ])
        form_layout.addRow("Tipo de Moeda:", self.tipo_moeda)
        
        # Campo para tipo personalizado
        self.tipo_personalizado = QLineEdit()
        self.tipo_personalizado.setPlaceholderText("Ex: CUSTOM/TOKEN")
        self.tipo_personalizado.setEnabled(False)
        form_layout.addRow("Tipo Personalizado:", self.tipo_personalizado)
        
        # Conectar sinal para habilitar campo personalizado
        self.tipo_moeda.currentTextChanged.connect(self.on_tipo_changed)
        
        layout.addLayout(form_layout)
        
        # Botões
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
        self.setLayout(layout)
    
    def on_tipo_changed(self, text):
        """Habilita/desabilita campo personalizado."""
        self.tipo_personalizado.setEnabled(text == "Outro")
    
    def load_config(self, config: PoolConfig):
        """Carrega configuração existente nos campos."""
        self.data_abertura.setDate(QDate.fromString(config.data_abertura, "yyyy-MM-dd"))
        self.valor_inicial.setText(str(config.valor_inicial))
        
        # Definir tipo de moeda
        index = self.tipo_moeda.findText(config.tipo_moeda)
        if index >= 0:
            self.tipo_moeda.setCurrentIndex(index)
        else:
            self.tipo_moeda.setCurrentText("Outro")
            self.tipo_personalizado.setText(config.tipo_moeda)
    
    def get_config(self) -> PoolConfig:
        """Retorna a configuração baseada nos campos preenchidos."""
        tipo = self.tipo_moeda.currentText()
        if tipo == "Outro":
            tipo = self.tipo_personalizado.text() or "CUSTOM/TOKEN"
        
        return PoolConfig(
            data_abertura=self.data_abertura.date().toString("yyyy-MM-dd"),
            valor_inicial=float(self.valor_inicial.text() or 0),
            tipo_moeda=tipo
        )