![Interface do app](assets/img/screenshot.png)

# collect-fee-pools

Aplicativo desktop moderno em Python para monitorar coletas de taxas em pools de liquidez DeFi com interface gráfica intuitiva — construído com PySide6 e com suporte a executáveis nativos para macOS e Windows.

## Funcionalidades

- **Gerenciamento de pools**:
  - Criar pools ilimitadas com configurações específicas (nome, par de tokens, valor inicial)
  - Editar e excluir pools com confirmação de segurança
  - Alternar entre pools via dropdown moderno

- **Monitoramento de Coletas**:
  - Registrar coletas com data e valor automaticamente
  - Calcular percentuais de taxas com base no valor inicial
  - Mostrar totais acumulados por pool e histórico completo

- **Interface moderna**:
  - Design clean com dropdown intuitivo
  - Tipografia otimizada, layout responsivo, botões com ícones

- **Gestão de dados**:
  - Persistência automática em arquivos CSV por pool
  - Migração automática de dados antigos
  - Exportação personalizada dos dados por pool

## Instalação

```bash
# Pré-requisitos
Python 3.13+
UV (gestor de pacotes Python)

# Instalar UV (se não tiver)
curl https://astral.sh/uv/install.sh | sh

# Instalação das dependências
uv sync
```

## Executando a aplicação

```bash
uv run main.py
```

## Gerar executável (macOS)

```bash
# Gerar binário
uv run build_final.py
```

## Solução de Problemas - macOS

### O aplicativo não abre com duplo-clique

Se ao tentar abrir o `.app` você receber a mensagem "O aplicativo não pode ser aberto" ou "app não confiável", isso ocorre porque o macOS bloqueia aplicativos baixados da internet ou não assinados digitalmente.

**Solução:**

Execute os seguintes comandos no Terminal:

```bash
# 1. Remover atributo de quarentena (arquivo baixado da internet)
xattr -d com.apple.quarantine /Applications/Collect\ Fee\ Pools.app

# 2. Dar permissão de execução para o binário
chmod -R +x /Applications/Collect\ Fee\ Pools.app/Contents/MacOS
```

Depois, tente abrir o aplicativo novamente com duplo-clique.

**Alternativa:**

Você também pode abrir o aplicativo usando **botão direito > Abrir** na primeira vez. Isso permite que você autorize a execução de aplicativos não verificados pela Apple.

**Por que isso acontece?**

- O `xattr -d` remove a marcação de "quarentena" que o macOS adiciona a arquivos baixados
- O `chmod +x` garante que o executável tenha permissão de execução
- O macOS Gatekeeper bloqueia apps não assinados por padrão por questões de segurança

## Como usar

1. Na primeira execução, a aplicação vai migrar dados antigos automaticamente.
2. Clique em “➕ Nova Pool” para criar sua primeira pool.
3. Registre coletas, visualize totais acumulados e acompanhe o histórico com facilidade.

---
