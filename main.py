"""
Monitor de Coletas - Pool de Liquidez
Aplicação para monitorar coletas de taxas em pools de liquidez.
"""

import sys
from PySide6.QtWidgets import QApplication

from gui.main_window import MonitorColetasApp


def main():
    """Função principal da aplicação."""
    app = QApplication(sys.argv)
    
    # Configurar estilo da aplicação
    app.setStyle('Fusion')
    
    # Criar e mostrar janela principal
    window = MonitorColetasApp()
    window.show()
    
    # Executar aplicação
    sys.exit(app.exec())


if __name__ == "__main__":
    main()