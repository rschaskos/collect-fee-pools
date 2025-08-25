import sys
import os
from time import sleep

def configurar_macos():
    """Configuração específica para macOS"""
    if sys.platform == "darwin":  # macOS
        try:
            # Tentar importar AppKit (nativo macOS)
            from AppKit import NSBundle, NSApplication, NSApplicationActivationPolicyRegular
            
            # Configurar bundle info
            bundle = NSBundle.mainBundle()
            if bundle:
                info = bundle.localizedInfoDictionary() or bundle.infoDictionary()
                if info:
                    info['CFBundleName'] = 'Collect Fee Pools'
                    info['CFBundleDisplayName'] = 'Collect Fee Pools'
                    info['CFBundleExecutable'] = 'Collect Fee Pools'
            
            # Configurar aplicação nativa
            app = NSApplication.sharedApplication()
            app.setActivationPolicy_(NSApplicationActivationPolicyRegular)
            
            print("✅ Configuração macOS aplicada com AppKit")
            return True
            
        except ImportError:
            print("⚠️  AppKit não disponível, usando fallback...")
            # Fallback: tentar via subprocess
            try:
                import subprocess
                # Definir nome do processo
                subprocess.run([
                    'defaults', 'write', 
                    f'com.python.python{sys.version_info.major}.{sys.version_info.minor}', 
                    'CFBundleName', 'Collect Fee Pools'
                ], check=False)
                return True
            except Exception as e:
                print(f"Fallback falhou: {e}")
                return False
    
    return False

def main():
    """Função principal otimizada com configuração macOS"""
    
    # CONFIGURAR MACOS PRIMEIRO (ANTES DE CRIAR QApplication)
    configurar_macos()
    
    try:
        # Importar apenas o necessário inicialmente
        from PySide6.QtWidgets import QApplication
        from PySide6.QtCore import Qt
        
        # Configurar variáveis de ambiente (macOS)
        if sys.platform == "darwin":
            os.environ['CFBundleName'] = 'Collect Fee Pools'
            os.environ['CFBundleDisplayName'] = 'Collect Fee Pools'
            # Força o nome do processo
            try:
                import setproctitle
                setproctitle.setproctitle('Collect Fee Pools')
            except ImportError:
                # Se não tiver setproctitle, continua sem problema
                pass
        
        # Criar aplicação
        app = QApplication(sys.argv)
        
        # ===== CONFIGURAR NOME DA APLICAÇÃO (MÚLTIPLAS TENTATIVAS) =====
        app.setApplicationName("Collect Fee Pools")
        app.setApplicationDisplayName("Collect Fee Pools")
        app.setApplicationVersion("2.0.0")
        app.setOrganizationName("DeFi Tools")
        app.setOrganizationDomain("collectfee.app")
        
        # Configuração adicional para macOS
        if sys.platform == "darwin":
            # Tentar configurar menu bar
            try:
                from PySide6.QtWidgets import QMenuBar
                app.setAttribute(Qt.AA_DontUseNativeMenuBar, False)
                # Força atualização do nome
                app.processEvents()
            except Exception as e:
                print(f"Configuração menu bar: {e}")
        
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
                icon = QIcon(icon_path)
                app.setWindowIcon(icon)
                break
        
        # Mostrar splash enquanto carrega
        from PySide6.QtWidgets import QSplashScreen
        
        # Splash personalizado
        pixmap = QPixmap(350, 200)
        pixmap.fill(QColor(52, 73, 94))
        
        splash = QSplashScreen(pixmap)
        splash.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        splash.setWindowTitle("Collect Fee Pools")  # Título do splash
        splash.showMessage(
            "🏊‍♂️ Collect Fee Pools v2.0\n\nCarregando aplicação...", 
            Qt.AlignCenter, 
            QColor(255, 255, 255)
        )
        splash.show()
        
        # Processar eventos para mostrar splash
        app.processEvents()
        sleep(1.5)
        
        # Importar app principal (demora mais)
        splash.showMessage(
            "🏊‍♂️ Collect Fee Pools v2.0\n\nInicializando interface...", 
            Qt.AlignCenter, 
            QColor(255, 255, 255)
        )
        app.processEvents()
        sleep(1.5)
        
        # Importar a classe correta
        from gui.main_window import MonitorColetasApp
        main_window = MonitorColetasApp()
        
        # ===== CONFIGURAR TÍTULO DA JANELA =====
        main_window.setWindowTitle("🏊‍♂️ Collect Fee Pools v2.0 - Monitor de Liquidez DeFi")
        
        # Aplicar ícone também na janela principal
        for icon_path in icon_paths:
            if os.path.exists(icon_path):
                main_window.setWindowIcon(QIcon(icon_path))
                break
        
        # Finalizar splash
        splash.showMessage(
            "🏊‍♂️ Collect Fee Pools v2.0\n\nPronto para usar!", 
            Qt.AlignCenter, 
            QColor(255, 255, 255)
        )
        app.processEvents()
        sleep(1)
        
        # Fechar splash e mostrar app
        if main_window:
            splash.finish(main_window)
            main_window.show()
            
            # Força atualização do nome no macOS (última tentativa)
            if sys.platform == "darwin":
                main_window.raise_()
                main_window.activateWindow()
                app.processEvents()
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