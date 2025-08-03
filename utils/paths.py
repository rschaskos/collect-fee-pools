import os
import sys
from pathlib import Path

def get_app_directory():
    """Retorna o diretório onde está o executável ou script."""
    if getattr(sys, 'frozen', False):
        # Se estiver executando como executável (PyInstaller)
        return os.path.dirname(sys.executable)
    else:
        # Se estiver executando como script Python
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_user_data_directory():
    """Retorna o diretório de dados do usuário para a aplicação."""
    if sys.platform == "darwin":  # macOS
        data_dir = Path.home() / "Library" / "Application Support" / "Monitor de Coletas"
    elif sys.platform == "win32":  # Windows
        data_dir = Path.home() / "AppData" / "Local" / "Monitor de Coletas"
    else:  # Linux
        data_dir = Path.home() / ".config" / "monitor-coletas"
    
    # Criar diretório se não existir
    data_dir.mkdir(parents=True, exist_ok=True)
    return str(data_dir)

def get_data_file_path(filename):
    """Retorna o caminho completo para um arquivo de dados."""
    # Usar diretório de dados do usuário em vez do diretório do app
    return os.path.join(get_user_data_directory(), filename)

def get_legacy_file_path(filename):
    """Retorna o caminho do arquivo no diretório do app (para migração)."""
    return os.path.join(get_app_directory(), filename)