#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

from time import sleep

def main():
    """Função principal otimizada"""
    
    try:
        # Importar apenas o necessário inicialmente
        from PySide6.QtWidgets import QApplication
        from PySide6.QtCore import Qt
        
        # Criar aplicação
        app = QApplication(sys.argv)
        app.setApplicationName("Collect-Fee")
        app.setApplicationVersion("2.0.0")
        
        # Configurar ícone da aplicação
        from PySide6.QtGui import QIcon, QPixmap, QColor
        
        # Tentar carregar ícone (com fallback)
        icon_paths = [
            'icon/favicon.ico',
            'icon/favicon.png', 
            'icon/favicon.icns',
            'assets/icon.ico',
            'assets/icon.png'
        ]
        
        for icon_path in icon_paths:
            if os.path.exists(icon_path):
                app.setWindowIcon(QIcon(icon_path))
                break
        
        # Mostrar splash enquanto carrega
        from PySide6.QtWidgets import QSplashScreen
        
        # Splash simples
        pixmap = QPixmap(300, 200)
        pixmap.fill(QColor(52, 73, 94))
        
        splash = QSplashScreen(pixmap)
        splash.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        splash.showMessage(
            "🏊‍♂️ Collect-Fee\n\nCarregando...", 
            Qt.AlignCenter, 
            QColor(255, 255, 255)
        )
        splash.show()
        
        # Processar eventos para mostrar splash
        app.processEvents()
        sleep(2)
        
        # Importar app principal (demora mais)
        splash.showMessage(
            "🏊‍♂️ Collect-Fee\n\nInicializando interface...", 
            Qt.AlignCenter, 
            QColor(255, 255, 255)
        )
        app.processEvents()
        sleep(2)
        
        # Importar a classe correta
        from gui.main_window import MonitorColetasApp
        main_window = MonitorColetasApp()
        
        # Aplicar ícone também na janela principal (se não foi definido globalmente)
        for icon_path in icon_paths:
            if os.path.exists(icon_path):
                main_window.setWindowIcon(QIcon(icon_path))
                break
        
        # Finalizar splash
        splash.showMessage(
            "🏊‍♂️ Collect-Fee\n\nFinalizando...", 
            Qt.AlignCenter, 
            QColor(255, 255, 255)
        )
        app.processEvents()
        
        # Fechar splash e mostrar app
        if main_window:
            splash.finish(main_window)
            main_window.show()
        else:
            splash.close()
            print("Erro: Não foi possível criar a janela principal")
            return 1
        
        # Executar aplicação
        return app.exec()
        
    except Exception as e:
        print(f"Erro ao iniciar aplicação: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())