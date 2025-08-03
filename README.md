# Monitor de Coletas - Pool de Liquidez

Uma aplicação desktop moderna para monitorar e gerenciar coletas de taxas em pools de liquidez de criptomoedas.

## 🚀 Funcionalidades

- **Interface Gráfica Moderna**: Desenvolvida com PySide6
- **Configuração de Pool**: Defina data de abertura, valor inicial e tipo de moeda
- **Registro de Coletas**: Adicione coletas com cálculo automático de taxas percentuais
- **Visualização de Dados**: Tabela com histórico completo e totais acumulados
- **Exportação**: Exporte dados para CSV com informações detalhadas
- **Persistência Segura**: Dados salvos automaticamente no diretório apropriado do sistema

## 📋 Requisitos

- Python 3.8 ou superior
- PySide6
- Pillow (para suporte a ícones)

## 🛠️ Instalação para Desenvolvimento

1. **Clone o repositório:**
```bash
git clone https://github.com/seu-usuario/collect-fee-pools.git
cd collect-fee-pools
```

2. **Crie um ambiente virtual:**
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. **Instale as dependências:**
```bash
pip install PySide6 Pillow
```

4. **Execute a aplicação:**
```bash
python main.py
```

## 📦 Criando Executável

### macOS

1. **Instale o PyInstaller:**
```bash
pip install pyinstaller
```

2. **Crie o executável:**
```bash
pyinstaller --clean --onefile --windowed main.py \
    --add-data "gui:gui" \
    --add-data "utils:utils" \
    --icon=icon/favicon.icns \
    --name "collect-fee"
```

3. **O app será criado em:**
```
dist/collect-fee.app
```

### Windows

1. **Instale o PyInstaller:**
```bash
pip install pyinstaller
```

2. **Crie o executável:**
```bash
pyinstaller --clean --onefile --windowed main.py ^
    --add-data "gui;gui" ^
    --add-data "utils;utils" ^
    --icon=icon/favicon.ico ^
    --name "collect-fee"
```

3. **O executável será criado em:**
```
dist/collect-fee.exe
```

## 📁 Estrutura do Projeto

```
collect-fee-pools/
├── main.py                 # Ponto de entrada da aplicação
├── core/
│   ├── __init__.py
│   └── monitor.py          # Lógica principal de negócio
├── models/
│   ├── __init__.py
│   ├── coleta.py           # Modelo de dados para coletas
│   └── pool_config.py      # Modelo de configuração da pool
├── gui/
│   ├── __init__.py
│   ├── main_window.py      # Janela principal
│   └── dialogs.py          # Diálogos de configuração
├── utils/
│   ├── __init__.py
│   └── paths.py            # Utilitários para caminhos de arquivos
├── icon/
│   ├── favicon.ico         # Ícone para Windows
│   └── favicon.icns        # Ícone para macOS
└── README.md
```

## 💾 Armazenamento de Dados

Os dados são armazenados automaticamente nos seguintes locais:

- **macOS**: `~/Library/Application Support/Monitor de Coletas/`
- **Windows**: `%USERPROFILE%/AppData/Local/Monitor de Coletas/`
- **Linux**: `~/.config/monitor-coletas/`

### Arquivos de Dados:
- `coletas.csv`: Histórico de todas as coletas
- `pool_config.csv`: Configuração da pool (data de abertura, valor inicial, moeda)

## 🔄 Migração Automática

A aplicação migra automaticamente dados existentes do diretório do projeto para o diretório de dados do usuário na primeira execução.

## 📊 Formato dos Dados

### Arquivo de Coletas (coletas.csv)
```csv
Data,Coleta_USD,Taxa_Percentual,Total_Acumulado_USD
2024-01-15,125.50,2.5100,125.50
2024-01-16,98.75,1.9750,224.25
```

### Arquivo de Configuração (pool_config.csv)
```csv
data_abertura,valor_inicial,tipo_moeda
2024-01-01,5000.0,USDC/ETH
```

## 🎯 Como Usar

1. **Primeira Execução**: Configure sua pool definindo:
   - Data de abertura
   - Valor inicial investido
   - Tipo de moeda/par

2. **Registrar Coletas**:
   - Clique em "Nova Coleta"
   - Insira a data e valor coletado
   - A taxa percentual é calculada automaticamente

3. **Visualizar Dados**:
   - Tabela mostra histórico completo
   - Totais acumulados são atualizados automaticamente

4. **Exportar Dados**:
   - Use "Exportar" para salvar relatório em CSV
   - Inclui configuração da pool e dados detalhados

## 🛡️ Segurança

- Dados armazenados localmente no computador do usuário
- Nenhuma informação é enviada para servidores externos
- Backup automático durante migrações

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🐛 Reportar Problemas

Se encontrar algum problema, por favor abra uma [issue](https://github.com/seu-usuario/collect-fee-pools/issues) com:

- Descrição detalhada do problema
- Passos para reproduzir
- Sistema operacional e versão do Python
- Screenshots (se aplicável)

## 📞 Suporte

Para dúvidas ou suporte, entre em contato através das issues do GitHub.

---

**Desenvolvido com ❤️ para a comunidade DeFi**
