# Setup da Máquina — Robô Legal One (Windows)

**Documento técnico para preparação de estação Windows que executará o robô de automação Legal One.**

- **Audiência:** equipe de TI / suporte técnico
- **Versão:** 1.0 — abril/2026
- **Repositório:** `dinizadv/claude-` (privado)
- **Escopo:** passos 1 a 9 (preparação do ambiente). Configuração de credenciais, seletores HTML e execução real são tratadas em sessão posterior, acompanhada pelo time de desenvolvimento.

---

## 1. Objetivo

Preparar uma estação Windows para executar o robô `legalone_robot_v1` (Python + Selenium). Ao final dos 9 passos, a máquina estará apta a receber configuração de credenciais e os primeiros testes acompanhados.

**Fora do escopo deste documento:**
- Criação do arquivo `.env` com credenciais do Legal One
- Mapeamento de seletores HTML específicos da interface Legal One
- Execução real contra o ambiente produtivo do Legal One

---

## 2. Pré-requisitos

### 2.1 Hardware e sistema operacional

- Windows 10 (build 1809+) ou Windows 11
- 8 GB de RAM (16 GB recomendado)
- 10 GB de espaço livre em disco
- Conexão estável com a internet

### 2.2 Permissões locais

- Conta com privilégios de **administrador local**
- Capacidade de instalar software via `winget` (Windows Package Manager)
- Permissão para alterar `ExecutionPolicy` do PowerShell no escopo `CurrentUser`

### 2.3 Acesso de rede

A máquina precisa alcançar (HTTPS porta 443):

- `python.org`, `pypi.org`, `files.pythonhosted.org` — instalação Python e dependências
- `github.com`, `objects.githubusercontent.com` — clone do repositório
- `microsoft.com`, `aka.ms`, `winget.azureedge.net` — winget e instaladores
- `update.microsoft.com` — atualização do Edge (Selenium Manager precisa do Edge atualizado)

Validar com a TI corporativa se há firewall, proxy ou inspeção SSL que bloqueiem esses endereços.

### 2.4 Acesso ao GitHub (atenção: repositório privado)

A pessoa que executa o `git clone` (passo 6) precisa de **uma destas opções**:

- **Opção A** — Conta GitHub com acesso de leitura ao repositório `dinizadv/claude-`.
- **Opção B (recomendada)** — Personal Access Token (PAT) com escopo `repo`, gerado pelo proprietário e fornecido ao técnico apenas no momento do clone. O PAT é colado como senha quando o git solicitar credenciais.
- **Opção C** — Chave SSH cadastrada na conta proprietária. Mais complexa, evitar para setup inicial.

Confirmar com o gestor antes de iniciar.

### 2.5 Rede corporativa (apenas se houver proxy)

Se a máquina opera atrás de proxy autenticado:

- `pip` precisa de configuração de proxy (`pip config set global.proxy http://usuario:senha@proxy:porta`)
- `git` precisa de configuração de proxy (`git config --global http.proxy http://usuario:senha@proxy:porta`)
- `winget` pode falhar — usar instaladores manuais (links fornecidos em cada passo)

---

## 3. Passos 1 a 9

### Passo 1 — Abrir PowerShell como Administrador

1. Pressione **Windows** e digite `powershell`.
2. Em **Windows PowerShell**, clique com o botão direito → **Executar como administrador**.
3. No prompt UAC, clique em **Sim**.

**Resultado esperado:** janela do PowerShell aberta com prompt similar a:

```
PS C:\WINDOWS\system32>
```

> O `PS` no início indica PowerShell. Se aparecer apenas `C:\Users\...>`, está em `cmd.exe`. Feche e repita.

---

### Passo 2 — Instalar Python 3.11

> **Atenção:** **não instale Python pela Microsoft Store.** A versão da Store cria aliases que confundem o ambiente. Use `winget` ou o instalador oficial.

```powershell
winget install --id Python.Python.3.11 --source winget --accept-source-agreements --accept-package-agreements
```

**Alternativa (sem winget):** baixar instalador oficial em <https://www.python.org/downloads/release/python-3119/>. Durante a instalação, **marcar obrigatoriamente**:

- `Add python.exe to PATH`
- `Install pip`

Após a instalação, **fechar e reabrir o PowerShell** (como administrador). O PATH só atualiza em sessões novas.

**Verificação:**

```powershell
python --version
pip --version
```

**Saída esperada (versões podem variar levemente):**

```
Python 3.11.9
pip 24.0 from C:\Users\<usuario>\AppData\Local\Programs\Python\Python311\Lib\site-packages\pip (python 3.11)
```

**Se `python --version` abrir a Microsoft Store:**

```powershell
Get-Command python | Format-List
```

Se o caminho contiver `WindowsApps`, é o alias da Store. Desativar em:

**Configurações → Apps → Configurações avançadas de aplicativos → Aliases de execução de aplicativo** → desligar `python.exe` e `python3.exe`.

Reabrir o PowerShell e tentar novamente.

---

### Passo 3 — Instalar Git

```powershell
winget install --id Git.Git --source winget --accept-source-agreements --accept-package-agreements
```

**Alternativa:** <https://git-scm.com/download/win>. Aceitar todas as configurações padrão.

**Fechar e reabrir o PowerShell.**

**Verificação:**

```powershell
git --version
```

**Saída esperada:**

```
git version 2.44.0.windows.1
```

(versão exata pode variar; qualquer 2.40+ serve)

---

### Passo 4 — Instalar Visual Studio Code

```powershell
winget install --id Microsoft.VisualStudioCode --source winget --accept-source-agreements --accept-package-agreements
```

**Alternativa:** <https://code.visualstudio.com/>.

Não é necessário abrir o VS Code agora. Será usado posteriormente para edição de arquivos de configuração.

---

### Passo 5 — Validar Microsoft Edge

O Microsoft Edge já vem instalado no Windows 10/11. Apenas confirmar a versão.

1. Abrir o Edge.
2. Menu (`...`) → **Ajuda e comentários** → **Sobre o Microsoft Edge**.
3. A página deve mostrar **versão 120 ou superior**.

Se a versão for inferior, deixar o Edge atualizar automaticamente nessa tela e reiniciar o navegador.

> **Observação técnica:** o Selenium 4 usa o Selenium Manager interno, que baixa o `msedgedriver` automaticamente conforme a versão do Edge. **Não baixar WebDriver manualmente.**

---

### Passo 6 — Clonar o repositório

Definir o caminho onde o projeto ficará. Sugestão padrão:

```powershell
cd $HOME\Documents
mkdir Projetos -Force
cd Projetos
```

Clonar:

```powershell
git clone https://github.com/dinizadv/claude-.git legalone
cd legalone
```

**Quando o git solicitar credenciais:**

- **Username:** usuário GitHub com acesso ao repositório
- **Password:** **NÃO usar a senha do GitHub.** Colar o **Personal Access Token (PAT)** descrito no item 2.4

**Verificação:**

```powershell
Get-ChildItem
```

**Saída esperada (lista parcial):**

```
CLAUDE.md
docs
legalone_robot_v1
.gitignore
```

---

### Passo 7 — Criar ambiente virtual Python

Entrar na pasta do robô:

```powershell
cd legalone_robot_v1
```

Criar o ambiente virtual:

```powershell
python -m venv .venv
```

Permitir execução de scripts no escopo do usuário (necessário apenas uma vez por usuário Windows):

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Quando perguntado, responder `S` (sim) ou `Y`.

Ativar o ambiente virtual:

```powershell
.\.venv\Scripts\Activate.ps1
```

**Resultado esperado:** o prompt agora exibe `(.venv)` no início:

```
(.venv) PS C:\Users\<usuario>\Documents\Projetos\legalone\legalone_robot_v1>
```

> Se aparecer `Não é possível carregar o arquivo ... porque a execução de scripts foi desabilitada`, repita o `Set-ExecutionPolicy` acima e confirme com `S`. Se a empresa bloqueia a política via GPO, a TI corporativa precisa liberar `RemoteSigned` para o usuário.

---

### Passo 8 — Instalar dependências do robô

Com o `(.venv)` ativo no prompt:

```powershell
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

> A flag `-e` instala em modo "editável", essencial para que o comando `legalone-robot` fique disponível. O sufixo `[dev]` traz as dependências de teste (`pytest`).

**Atrás de proxy corporativo:**

```powershell
pip install --proxy http://usuario:senha@proxy:porta -e ".[dev]"
```

**Resultado esperado:** sequência de mensagens `Successfully installed ...`, sem nenhum `ERROR`.

**Pacotes principais que serão instalados:**

- `selenium` 4.20+ — automação do navegador
- `openpyxl` 3.1+ — leitura/escrita de XLSX
- `python-dateutil` 2.9+ — manipulação de datas
- `pytest` 8+ — execução de testes

---

### Passo 9 — Verificação final

Ainda na pasta `legalone_robot_v1`, com `(.venv)` ativo:

**9.1 — Testar o comando da CLI:**

```powershell
legalone-robot --help
```

**Saída esperada:** texto de ajuda mostrando os parâmetros aceitos:

```
usage: legalone-robot [-h] --input INPUT --config CONFIG --selectors SELECTORS [--dry-run]

Robô determinístico Legal One — V1

options:
  -h, --help            show this help message and exit
  --input INPUT         Planilha XLSX/XLSM de entrada
  --config CONFIG       Arquivo JSON de configuração
  --selectors SELECTORS Arquivo JSON com seletores da UI
  --dry-run             Somente valida a planilha
```

**9.2 — Rodar a suíte de testes existente:**

```powershell
pytest -v
```

**Saída esperada:** todos os testes com `PASSED`, terminando em algo similar a:

```
======================== X passed in Y.YZs ========================
```

✅ **Se ambos comandos funcionaram, a máquina está pronta.**

---

## 4. Critério de aceite — o que entregar de volta

Para confirmar conclusão, enviar ao gestor:

**1. Print do PowerShell** mostrando o resultado de:

```powershell
legalone-robot --help
```

**2. Print do PowerShell** mostrando o resultado de:

```powershell
pytest -v
```

(com todos os testes em `PASSED`)

**3. Confirmação textual das versões instaladas:**

```powershell
python --version
git --version
pip list | Select-String -Pattern "selenium|openpyxl|pytest|dateutil"
```

Copiar a saída desses comandos e enviar.

---

## 5. Solução de problemas comuns

### `winget` não é reconhecido

Windows desatualizado ou sem App Installer. Atualizar via Windows Update ou instalar **App Installer** pela Microsoft Store. Como contorno imediato, usar os instaladores manuais indicados em cada passo.

### `python` abre a Microsoft Store em vez do Python real

Aliases da Store ativos. Desativar em **Configurações → Apps → Configurações avançadas de aplicativos → Aliases de execução de aplicativo** (ver Passo 2). Alternativa: usar o lançador oficial `py` em lugar de `python`.

### `git clone` falha com `Authentication failed`

A senha do GitHub não funciona em clone HTTPS desde 2021. É preciso usar Personal Access Token (PAT). Gerar em: GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic) → **Generate new token (classic)**, com escopo `repo`.

### `Activate.ps1` falha com erro de política de execução

Executar `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` antes de ativar (ver Passo 7). Se a empresa aplica política mais restritiva via GPO, a TI corporativa precisa liberar `RemoteSigned` no escopo do usuário.

### `pip install` falha com erro SSL

Geralmente indica firewall corporativo interceptando HTTPS. Soluções, em ordem:

1. Configurar certificados corporativos no `pip` (`pip config set global.cert <caminho-do-certificado.pem>`)
2. Solicitar à TI corporativa liberação de acesso a `pypi.org` e `files.pythonhosted.org`
3. Como último recurso, `pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -e ".[dev]"` (não recomendado para máquinas de produção)

### Testes (`pytest`) falham

Capturar a saída completa do `pytest -v` e enviar ao gestor. **Não tentar correção autônoma** — falhas em teste indicam problema de ambiente que precisa diagnóstico específico.

### Comando `legalone-robot` não encontrado após `pip install`

Verificar se o `(.venv)` está ativo no prompt. Se sim, executar:

```powershell
pip install -e ".[dev]" --force-reinstall
```

Se ainda assim falhar, verificar que o passo 8 foi executado **dentro da pasta `legalone_robot_v1`** (não na raiz `legalone`).

---

## 6. Próximos passos (após validação)

Após o setup confirmado pelos prints do passo 9, em sessão acompanhada pelo gestor e pelo time de desenvolvimento:

1. Criação do arquivo `.env` com credenciais do Legal One (nunca versionado).
2. Recebimento e configuração do arquivo `selectors.json` específico do Legal One.
3. Primeira execução em modo `--dry-run` com planilha de exemplo.
4. Validação da extração e do preenchimento assistido em ambiente de homologação.

---

## 7. Contato e suporte

Para qualquer erro não coberto neste documento:

1. **Parar a execução** no ponto do erro.
2. **Capturar a mensagem literal** (texto completo, não apenas descrição).
3. **Enviar ao gestor do projeto** com indicação do passo em que ocorreu.

Não tentar correções "criativas" em arquivos do projeto, configurações de proxy ou políticas de segurança. Vários erros de setup indicam restrições corporativas legítimas que precisam de tratamento específico pela TI da empresa, não contorno técnico.
