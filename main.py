import sys
import os
from time import sleep

def configurar_macos():
    """Configuração específica para macOS"""
    if sys.platform == "darwin":
        try:
            from AppKit import NSBundle, NSApplication, NSApplicationActivationPolicyRegular
            
            bundle = NSBundle.mainBundle()
            if bundle:
                info = bundle.localizedInfoDictionary() or bundle.infoDictionary()
                if info:
                    info['CFBundleName'] = 'Collect Fee Pools'
                    info['CFBundleDisplayName'] = 'Collect Fee Pools'
                    info['CFBundleExecutable'] = 'Collect Fee Pools'
            
            app = NSApplication.sharedApplication()
            app.setActivationPolicy_(NSApplicationActivationPolicyRegular)
            
            return True
            
        except ImportError:
            os.environ.update({
                'CFBundleName': 'Collect Fee Pools',
                'CFBundleDisplayName': 'Collect Fee Pools',
            })
            return True
        except Exception:
            return False
    
    return False

def main():
    """Função principal - baseada exatamente no que funcionou no debug"""
    
    try:
        # Configuração macOS
        configurar_macos()
        
        # Imports Qt
        from PySide6.QtWidgets import QApplication, QSplashScreen
        from PySide6.QtCore import Qt
        from PySide6.QtGui import QPixmap, QColor, QIcon
        
        # Criar aplicação
        app = QApplication(sys.argv)
        app.setApplicationName("Collect Fee Pools")
        app.setApplicationDisplayName("Collect Fee Pools")
        app.setApplicationVersion("2.0.0")
        app.setOrganizationName("DeFi Tools")
        app.setOrganizationDomain("collectfee.app")
        
        # Configuração adicional para macOS
        if sys.platform == "darwin":
            app.setAttribute(Qt.AA_DontUseNativeMenuBar, False)
            app.processEvents()
        
        # Configurar ícone
        icon_paths = [
            'icon/uniswap.png',
            'icon/favicon.ico',
            'icon/favicon.icns',
        ]

        for icon_path in icon_paths:
            if os.path.exists(icon_path):
                icon = QIcon(icon_path)
                app.setWindowIcon(icon)
                break
        
        # Splash screen
        pixmap = QPixmap(350, 200)
        pixmap.fill(QColor(52, 73, 94))
        
        splash = QSplashScreen(pixmap)
        splash.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        splash.setWindowTitle("Collect Fee Pools")
        splash.showMessage(
            "Collect Fee Pools v2.0\n\nCarregando aplicação...",
            Qt.AlignCenter,
            QColor(255, 255, 255)
        )
        splash.show()
        app.processEvents()
        
        sleep(1.5)
        
        # Importar e criar aplicação principal
        splash.showMessage(
            "Collect Fee Pools v2.0\n\nInicializando interface...",
            Qt.AlignCenter,
            QColor(255, 255, 255)
        )
        app.processEvents()
        sleep(1.5)
        
        from gui.main_window import MonitorColetasApp
        main_window = MonitorColetasApp()
        
        # Configurar janela
        main_window.setWindowTitle("Collect Fee Pools")
        
        # Aplicar ícone na janela
        for icon_path in icon_paths:
            if os.path.exists(icon_path):
                main_window.setWindowIcon(QIcon(icon_path))
                break
        
        # Finalizar splash
        splash.showMessage(
            "Collect Fee Pools v2.0\n\nPronto para usar!",
            Qt.AlignCenter,
            QColor(255, 255, 255)
        )
        app.processEvents()
        sleep(1)
        
        # Mostrar aplicação
        splash.finish(main_window)
        main_window.show()
        
        # Ativação macOS
        if sys.platform == "darwin":
            main_window.raise_()
            main_window.activateWindow()
            app.processEvents()
        
        # Executar
        return app.exec()
        
    except Exception as e:
        print(f"Erro ao iniciar aplicação: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())