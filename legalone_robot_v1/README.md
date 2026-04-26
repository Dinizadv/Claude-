# Robô determinístico Legal One — V1

Este pacote implementa a primeira fase do robô de lançamentos por planilha.

Objetivo:
1. Ler uma planilha estruturada de lançamentos.
2. Validar linha a linha.
3. Executar o lançamento no Legal One por interface web, de forma determinística.
4. Registrar o resultado em log e devolver o ID gerado, quando houver.

## Observações importantes
- A V1 foi desenhada para **lançamentos novos**, não para revisão inteligente.
- A camada de IA deve abastecer a planilha, nunca atuar diretamente no sistema.
- O código foi estruturado para usar Selenium, em linha com o executável atual do escritório.
- Os seletores da tela do Legal One ficaram isolados em `selectors.example.json`. Eles devem ser ajustados com base na tela real.
- O modo `--dry-run` valida a planilha inteira sem abrir o navegador.

## Estrutura
- `src/legalone_robot/cli.py`: entrada de linha de comando.
- `src/legalone_robot/excel_io.py`: leitura da planilha.
- `src/legalone_robot/validators.py`: validações determinísticas.
- `src/legalone_robot/browser.py`: automação Selenium.
- `src/legalone_robot/orchestrator.py`: fluxo de lote.
- `examples/launcher_template.xlsx`: modelo de planilha de entrada.
- `examples/config.example.json`: exemplo de configuração, sem credenciais.
- `examples/selectors.example.json`: mapa de seletores a ser ajustado.
- `docs/achados_arquivos_compartilhados.md`: consolidação do que foi inferido dos arquivos compartilhados.

## Execução
### 1) Instalar dependências
```bash
pip install -r requirements.txt
```

### 2) Preparar configuração
Copie `examples/config.example.json` para `config.local.json` e preencha:
- usuário
- senha
- URL base do Legal One
- URL da tela de nova hora trabalhada, se já conhecida
- modo headless ou não

### 3) Ajustar seletores
Copie `examples/selectors.example.json` para `selectors.local.json` e ajuste os campos:
- login
- navegação até nova hora
- campos do formulário
- botão salvar
- leitura do ID gerado
- mensagens de erro

### 4) Rodar em validação seca
```bash
python -m legalone_robot.cli --input examples/launcher_template.xlsx --config config.local.json --selectors selectors.local.json --dry-run
```

### 5) Rodar o lote real
```bash
python -m legalone_robot.cli --input examples/launcher_template.xlsx --config config.local.json --selectors selectors.local.json
```

## Colunas esperadas na planilha
- linha_id
- executante
- data_inicio
- hora_inicio
- duracao_hhmm
- cliente_principal
- negociacao
- descricao_negociacao
- pasta
- nome_pasta
- tipo_subtipo
- descricao
- cobravel
- observacoes_executante
- gerente_conta
- grupo
- pode_lancar
- motivo_bloqueio
- status_execucao
- id_lancamento_retorno
- mensagem_retorno

## Regras operacionais da V1
- Não tentar corrigir conteúdo ambíguo.
- Bloquear linhas sem data de início, duração, executante, tipo/subtipo ou descrição.
- Usar `00:00` como hora padrão quando a planilha vier em branco, em linha com o procedimento descrito no projeto.
- Continuar o lote após falha de uma linha.
- Nunca executar a linha se a página carregada não corresponder ao formulário esperado.
- Nunca registrar credenciais em log.
