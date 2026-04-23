#!/usr/bin/env python3
"""
Build final multiplataforma - macOS, Windows, Linux
"""

import os
import subprocess
import sys
import shutil
from pathlib import Path

def executar_comando(comando):
    """Executa comando"""
    try:
        resultado = subprocess.run(comando, capture_output=True, text=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Erro: {e.stderr}")
        return False

def gerar_spec_macos():
    """Gera .spec para macOS"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

import sys
from pathlib import Path

project_root = Path.cwd()

datas = [
    (str(project_root / 'gui'), 'gui'),
    (str(project_root / 'core'), 'core'),
    (str(project_root / 'models'), 'models'),
    (str(project_root / 'utils'), 'utils'),
]

# Incluir ícones
for icon_dir in ['icon', 'assets']:
    icon_path = project_root / icon_dir
    if icon_path.exists():
        datas.append((str(icon_path), icon_dir))

hiddenimports = [
    'PySide6.QtCore',
    'PySide6.QtWidgets',
    'PySide6.QtGui',
    'models.coleta',
    'models.pool_config',
    'core.monitor',
    'gui.main_window',
    'gui.dialogs',
    'gui.about_dialog',
    'utils.paths',
    'utils.styles',
]

# Excluir módulos Qt não utilizados para reduzir tamanho do build
excludes = [
    # Módulos Qt6 definitivamente NÃO usados
    'PySide6.QtWebEngine',
    'PySide6.QtWebEngineCore',
    'PySide6.QtWebEngineWidgets',
    'PySide6.QtWebChannel',
    'PySide6.QtSql',
    'PySide6.QtNetwork',
    'PySide6.QtMultimedia',
    'PySide6.QtMultimediaWidgets',
    'PySide6.QtPrintSupport',
    'PySide6.Qt3DCore',
    'PySide6.Qt3DRender',
    'PySide6.Qt3DInput',
    'PySide6.QtCharts',
    'PySide6.QtDataVisualization',
    'PySide6.QtQuick',
    'PySide6.QtQml',
    # Módulos Python padrão desnecessários
    'tkinter',
    'matplotlib',
    'numpy',
    'scipy',
    'pandas',
    'PIL',
    'pytest',
    'unittest',
]

a = Analysis(
    ['main.py'],
    pathex=[str(project_root)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excludes,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='collect-fee',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=True,
    upx=False,
    upx_exclude=[],
    name='collect-fee',
)

app = BUNDLE(
    coll,
    name='Collect Fee Pools.app',
    icon='icon/favicon.icns' if (project_root / 'icon' / 'favicon.icns').exists() else None,
    bundle_identifier='com.defitools.collectfeepools',
    info_plist={
        'CFBundleName': 'Collect Fee Pools',
        'CFBundleDisplayName': 'Collect Fee Pools',
        'CFBundleVersion': '2.0.0',
        'CFBundleShortVersionString': '2.0.0',
        'NSHighResolutionCapable': True,
        'LSMinimumSystemVersion': '10.14.0',
        'NSRequiresAquaSystemAppearance': False,
        'LSBackgroundOnly': False,
    }
)
'''

    with open('collect-fee.spec', 'w') as f:
        f.write(spec_content)

def gerar_spec_windows():
    """Gera .spec para Windows"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

import sys
from pathlib import Path

project_root = Path.cwd()

datas = [
    (str(project_root / 'gui'), 'gui'),
    (str(project_root / 'core'), 'core'),
    (str(project_root / 'models'), 'models'),
    (str(project_root / 'utils'), 'utils'),
]

# Incluir ícones
for icon_dir in ['icon', 'assets']:
    icon_path = project_root / icon_dir
    if icon_path.exists():
        datas.append((str(icon_path), icon_dir))

hiddenimports = [
    'PySide6.QtCore',
    'PySide6.QtWidgets',
    'PySide6.QtGui',
    'PySide6.QtSvg',
    'pyside6_plugins',
    'models.coleta',
    'models.pool_config',
    'core.monitor',
    'gui.main_window',
    'gui.dialogs',
    'gui.about_dialog',
    'utils.paths',
    'utils.styles',
]

# Excluir módulos Qt não utilizados para reduzir tamanho do build
excludes = [
    # Módulos Qt6 definitivamente NÃO usados
    'PySide6.QtWebEngine',
    'PySide6.QtWebEngineCore',
    'PySide6.QtWebEngineWidgets',
    'PySide6.QtWebChannel',
    'PySide6.QtSql',
    'PySide6.QtNetwork',
    'PySide6.QtMultimedia',
    'PySide6.QtMultimediaWidgets',
    'PySide6.QtPrintSupport',
    'PySide6.Qt3DCore',
    'PySide6.Qt3DRender',
    'PySide6.Qt3DInput',
    'PySide6.QtCharts',
    'PySide6.QtDataVisualization',
    'PySide6.QtQuick',
    'PySide6.QtQml',
    # Módulos Python padrão desnecessários
    'tkinter',
    'matplotlib',
    'numpy',
    'scipy',
    'pandas',
    'PIL',
    'pytest',
    'unittest',
]

a = Analysis(
    ['main.py'],
    pathex=[str(project_root)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excludes,
    win_no_prefer_redirects=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='collect-fee.exe',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,
    upx=False,
    console=False,
    icon='icon/favicon.ico' if (project_root / 'icon' / 'favicon.ico').exists() else None,
    disable_windowed_traceback=False,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=True,
    upx=False,
    upx_exclude=[],
    name='collect-fee',
)
'''

    with open('collect-fee.spec', 'w') as f:
        f.write(spec_content)

def gerar_spec_linux():
    """Gera .spec para Linux"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

import sys
from pathlib import Path

project_root = Path.cwd()

datas = [
    (str(project_root / 'gui'), 'gui'),
    (str(project_root / 'core'), 'core'),
    (str(project_root / 'models'), 'models'),
    (str(project_root / 'utils'), 'utils'),
]

# Incluir ícones
for icon_dir in ['icon', 'assets']:
    icon_path = project_root / icon_dir
    if icon_path.exists():
        datas.append((str(icon_path), icon_dir))

hiddenimports = [
    'PySide6.QtCore',
    'PySide6.QtWidgets',
    'PySide6.QtGui',
    'models.coleta',
    'models.pool_config',
    'core.monitor',
    'gui.main_window',
    'gui.dialogs',
    'gui.about_dialog',
    'utils.paths',
    'utils.styles',
]

# Excluir módulos Qt não utilizados para reduzir tamanho do build
excludes = [
    # Módulos Qt6 definitivamente NÃO usados
    'PySide6.QtWebEngine',
    'PySide6.QtWebEngineCore',
    'PySide6.QtWebEngineWidgets',
    'PySide6.QtWebChannel',
    'PySide6.QtSql',
    'PySide6.QtNetwork',
    'PySide6.QtMultimedia',
    'PySide6.QtMultimediaWidgets',
    'PySide6.QtPrintSupport',
    'PySide6.Qt3DCore',
    'PySide6.Qt3DRender',
    'PySide6.Qt3DInput',
    'PySide6.QtCharts',
    'PySide6.QtDataVisualization',
    'PySide6.QtQuick',
    'PySide6.QtQml',
    # Módulos Python padrão desnecessários
    'tkinter',
    'matplotlib',
    'numpy',
    'scipy',
    'pandas',
    'PIL',
    'pytest',
    'unittest',
]

a = Analysis(
    ['main.py'],
    pathex=[str(project_root)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excludes,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='collect-fee',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,
    upx=False,
    console=False,
    icon='icon/favicon.ico' if (project_root / 'icon' / 'favicon.ico').exists() else None,
    disable_windowed_traceback=False,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=True,
    upx=False,
    upx_exclude=[],
    name='collect-fee',
)
'''

    with open('collect-fee.spec', 'w') as f:
        f.write(spec_content)

def detectar_plataforma():
    """Detecta a plataforma atual"""
    if sys.platform == "darwin":
        return "macos"
    elif sys.platform == "win32":
        return "windows"
    elif sys.platform == "linux":
        return "linux"
    else:
        return "unknown"

def preparar_icone_macos():
    """Prepara ícone .icns para macOS"""
    icns_path = Path('icon/favicon.icns')
    ico_path = Path('icon/favicon.ico')

    if not icns_path.exists() and ico_path.exists():
        print("Convertendo .ico para .icns...")
        try:
            resultado = subprocess.run([
                'sips', '-s', 'format', 'icns',
                str(ico_path), '--out', str(icns_path)
            ], capture_output=True, text=True)

            if resultado.returncode == 0:
                print(f"Icone convertido: {icns_path}")
            else:
                print(f"Falha na conversao: {resultado.stderr}")
        except Exception as e:
            print(f"Erro ao converter icone: {e}")
    elif icns_path.exists():
        print(f"Icone .icns encontrado: {icns_path}")
    else:
        print("Nenhum arquivo .icns encontrado")

def main():
    """Build final multiplataforma"""
    plataforma = detectar_plataforma()

    print(f"BUILD - COLLECT FEE POOLS ({plataforma.upper()})")

    if plataforma == "unknown":
        print("[ERRO] Plataforma não suportada")
        return 1

    # Verificar arquivo principal
    if not os.path.exists('main.py'):
        print("[ERRO] main.py não encontrado!")
        return 1

    # Preparativos específicos da plataforma
    if plataforma == "macos":
        preparar_icone_macos()

    # Limpar
    print("Limpando builds antigos...")
    for item in ['build', 'dist', '*.spec']:
        for path in Path('.').glob(item):
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()

    # Gerar .spec apropriado
    print("Gerando .spec...")
    if plataforma == "macos":
        gerar_spec_macos()
    elif plataforma == "windows":
        gerar_spec_windows()
    elif plataforma == "linux":
        gerar_spec_linux()

    # Build
    print("Executando build...")
    if not executar_comando(['pyinstaller', '--clean', '--noconfirm', 'collect-fee.spec']):
        print("[ERRO] Falha no build")
        return 1

    # Verificar resultado
    print("Build concluido com sucesso!")

    if plataforma == "macos":
        app_path = Path('dist/Collect Fee Pools.app')
        if app_path.exists():
            print(f"Aplicacao: {app_path}")
            print("\nTESTE:")
            print("   open 'dist/Collect Fee Pools.app'")
            return 0
    elif plataforma == "windows":
        exe_path = Path('dist/collect-fee/collect-fee.exe')
        if exe_path.exists():
            print(f"Executavel: {exe_path}")
            return 0
    elif plataforma == "linux":
        exe_path = Path('dist/collect-fee/collect-fee')
        if exe_path.exists():
            print(f"Executavel: {exe_path}")
            return 0

    print("Aplicacao nao foi criada")
    return 1

if __name__ == "__main__":
    sys.exit(main())