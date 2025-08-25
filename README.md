# 🏊‍♂️ Monitor de Coletas - Pools de Liquidez

Uma aplicação moderna e intuitiva para monitorar coletas de taxas de múltiplas pools de liquidez, desenvolvida em Python com interface gráfica PySide6.

## Funcionalidades Principais

### **Gerenciamento de Múltiplas Pools**
- **Criar pools ilimitadas** com configurações individuais
- **Editar pools existentes** (nome, par de moedas, valor inicial)
- **Excluir pools** com confirmação de segurança
- **Alternar entre pools** via dropdown moderno

### **Monitoramento de Coletas**
- **Registrar coletas** com data e valor
- **Cálculo automático de taxas** baseado no valor inicial
- **Totais acumulados** por pool
- **Histórico completo** de todas as coletas

### **Interface Moderna**
- **Design clean** com dropdown para seleção de pools
- **Cores profissionais** e tipografia otimizada
- **Layout responsivo** e intuitivo
- **Botões com ícones** para ações rápidas

### **Gestão de Dados**
- **Persistência automática** em arquivos CSV
- **Migração automática** de dados antigos
- **Exportação personalizada** por pool
- **Arquivos separados** para cada pool

## Instalação

### Pré-requisitos
```bash
Python 3.8+
PySide6
```

### Instalação das Dependências
```bash
pip install PySide6 pyinstaller pillow setproctitle pyobjc-framework-Cocoa
```

### Executar a Aplicação
```bash
python main.py
```

## Gerar Executável (macOS)

```bash
# Instalar PyInstaller
pip install pyinstaller

# Gerar aplicação
python build_final.py
```

## Como Usar

### 1️⃣ **Primeira Execução**
- Execute a aplicação
- Dados antigos serão migrados automaticamente
- Crie sua primeira pool clicando em "➕ Nova Pool"

### 2️⃣ **Gerenciar Pools**
```
🏊‍♂️ [Pool Principal - USDC/ETH  ▼] ➕ ✏️ 🗑️
```
- **Dropdown**: Selecione a pool ativa
- **Nova Pool**: Criar nova pool
- **Editar**: Modificar pool selecionada
- **Excluir**: Remover pool (com confirmação)

### 3️⃣ **Registrar Coletas**
- Selecione a pool desejada no dropdown
- Clique em "➕ Nova Coleta"
- Preencha data e valor
- Taxa será calculada automaticamente

### 4️⃣ **Exportar Dados**
- Selecione a pool no dropdown
- Clique em "📊 Exportar CSV"
- Escolha local para salvar

## 🔄 Migração de Dados

A aplicação detecta automaticamente dados do formato antigo e migra para o novo sistema:

- ✅ **pool_config.csv** → **pools_config.csv**
- ✅ **coletas.csv** → **pool_[UUID]_coletas.csv**
- ✅ **Configurações preservadas**
- ✅ **Histórico mantido**

## Capturas de Tela

### Interface Principal
```
┌─────────────────────────────────────────────────────┐
│        🏊‍♂️ Monitor de Coletas - Pools de Liquidez        │
├─────────────────────────────────────────────────────┤
│ 🏊 Gerenciamento de Pools                           │
│ Pool Ativa: [USDC/ETH - Uniswap    ▼] ➕ ✏️ 🗑️      │
├─────────────────────────────────────────────────────┤
│ 💰 Coletas da Pool Ativa                           │
│ [➕ Nova Coleta]              [📊 Exportar] [🗑️ Limpar] │
├─────────────────────────────────────────────────────┤
│ Data      │ Valor (USD) │ Taxa (%)  │ Acumulado    │
│ 15/01     │ $125.50     │ 12.5500%  │ $125.50      │
│ 20/01     │ $89.30      │ 8.9300%   │ $214.80      │
├─────────────────────────────────────────────────────┤
│ Total: 2 coletas    $214.80    Taxa: 21.48%        │
└─────────────────────────────────────────────────────┘
```

## Tecnologias Utilizadas

- **Python 3.8+** - Linguagem principal
- **PySide6** - Interface gráfica moderna
- **CSV** - Persistência de dados
- **UUID** - Identificadores únicos
- **PyInstaller** - Geração de executáveis

## Funcionalidades Avançadas

### **Cálculos Automáticos**
- Taxa percentual baseada no valor inicial
- Totais acumulados por pool
- Soma de taxas por período

### **Segurança de Dados**
- Backup automático antes de migrações
- Confirmações para ações destrutivas
- Validação de dados de entrada

### **Performance**
- Carregamento sob demanda
- Cache de dados da pool ativa
- Otimização para múltiplas pools

## Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Changelog

### v2.0.0 - Multi-Pool Support
- Suporte a múltiplas pools simultâneas
- Interface modernizada com dropdown
- Arquitetura refatorada para escalabilidade
- Migração automática de dados antigos
- Sistema de arquivos separados por pool

### v1.0.0 - Initial Release
- Monitoramento de pool única
- Cálculo de taxas automático
- Persistência em CSV
- Interface gráfica básica

## Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🆘 Suporte

Para dúvidas, sugestões ou problemas:

1. **Issues**: Abra uma issue no GitHub
2. **Discussões**: Use as discussões do repositório
3. **Email**: Entre em contato diretamente

---

**Desenvolvido para a comunidade DeFi**

*Monitore suas pools de liquidez com eficiência e estilo!* 🚀
