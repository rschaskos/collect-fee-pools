#!/usr/bin/env python3
"""
Build final definitivo - baseado no que funcionou no debug
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

def gerar_spec_final():
    """Gera .spec final com as configurações que funcionaram"""
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

a = Analysis(
    ['main.py'],
    pathex=[str(project_root)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
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
    strip=False,
    upx=False,
    console=True,  # CRÍTICO: Manter console=True
    disable_windowed_traceback=False,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
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

def main():
    """Build final"""
    print("🚀 BUILD DEFINITIVO - COLLECT FEE POOLS")
    
    if sys.platform != "darwin":
        print("❌ Específico para macOS")
        return 1
    
    # Verificar arquivo principal
    if not os.path.exists('main.py'):
        print("❌ main.py não encontrado!")
        return 1
    
    # Verificar se existe .icns, senão converter de .ico
    icns_path = Path('icon/favicon.icns')
    ico_path = Path('icon/favicon.ico')
    
    if not icns_path.exists() and ico_path.exists():
        print("🔄 Convertendo .ico para .icns...")
        try:
            # Usar sips (nativo do macOS) para converter
            resultado = subprocess.run([
                'sips', '-s', 'format', 'icns', 
                str(ico_path), '--out', str(icns_path)
            ], capture_output=True, text=True)
            
            if resultado.returncode == 0:
                print(f"✅ Ícone convertido: {icns_path}")
            else:
                print(f"⚠️ Falha na conversão: {resultado.stderr}")
                print("   Continuando sem ícone personalizado...")
        except Exception as e:
            print(f"⚠️ Erro ao converter ícone: {e}")
    elif icns_path.exists():
        print(f"✅ Ícone .icns encontrado: {icns_path}")
    else:
        print("⚠️ Nenhum arquivo de ícone encontrado")
    
    # Limpar
    print("🧹 Limpando...")
    for item in ['build', 'dist', '*.spec']:
        for path in Path('.').glob(item):
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()
    
    # Gerar .spec
    print("📝 Gerando .spec...")
    gerar_spec_final()
    
    # Build
    print("🔨 Executando build...")
    if not executar_comando(['pyinstaller', '--clean', '--noconfirm', 'collect-fee.spec']):
        print("❌ Falha no build")
        return 1
    
    # Verificar resultado
    app_path = Path('dist/Collect Fee Pools.app')
    if app_path.exists():
        # Verificar se o ícone foi incluído
        icon_resources = app_path / 'Contents' / 'Resources'
        if (icon_resources / 'icon-windowed.icns').exists():
            print("✅ Ícone incluído no bundle")
        
        print("✅ Build concluído com sucesso!")
        print(f"📱 Aplicação: {app_path}")
        print("\n🎯 TESTE:")
        print("   open 'dist/Collect Fee Pools.app'")
        return 0
    else:
        print("❌ Aplicação não foi criada")
        return 1

if __name__ == "__main__":
    sys.exit(main())