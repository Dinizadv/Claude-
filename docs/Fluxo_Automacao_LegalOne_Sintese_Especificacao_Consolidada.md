# Fluxo de Automação Legal One — Síntese Executiva e Especificação Operacional Consolidada

**Projeto:** Automação de extração, revisão, aprovação, correção e liberação de lançamentos de horas no Legal One  
**Finalidade:** Documento-base para submissão ao Codex e ao Claude Code  
**Formato:** Markdown  
**Versão:** Consolidada e revisada  
**Escopo:** Extração de dados, organização em planilha, triagem por IA, revisão humana, geração de plano de ação e execução assistida/API/RPA no Legal One

---

## 1) Síntese Executiva

Este documento define uma arquitetura **incremental, auditável e segura** para automatizar o fluxo de controle de horas no Legal One, mantendo o modelo operacional atual de revisão em planilha e incorporando IA para **triagem, classificação e sugestão**.

Premissas principais:

- Legal One é **fonte primária** e **destino final** dos dados.
- A base bruta deve ser preservada e rastreável.
- A IA **sugere**; o humano **valida**; o robô **executa**.
- Campos sensíveis só podem ser alterados com autorização humana explícita.
- Implementação deve seguir evolução por fases (do `dry_run` ao `auto_safe`).

Decisões operacionais centrais:

- `APROVAR_SEM_ACAO`
- `CORRIGIR_E_LIBERAR`
- `DEVOLVER_PARA_CORRECAO`
- `REVISAR_HUMANAMENTE`

A execução deve ser guiada por **manifest de ações** e controles de autorização por linha, com logs e possibilidade de rollback.

---

## 2) Objetivo Geral

Construir automação para:

1. Extrair dados do Legal One.
2. Organizar/normalizar em planilha operacional.
3. Submeter à IA para triagem.
4. Gerar planilha de revisão humana.
5. Importar retorno humano.
6. Gerar plano de ação estruturado.
7. Preparar execução (alterar/criar hora, alterar/criar tarefa, mudar status, devolver executante).
8. Executar por API/RPA com validação, logs e trilha de auditoria.

---

## 3) Princípios Obrigatórios

### 3.1 Legal One como fonte e destino

```text
Legal One
↓
Exportação de horas/tarefas/status
↓
Planilha bruta preservada
↓
Normalização e triagem
↓
Modelo de IA
↓
Planilha de revisão humana
↓
Retorno validado
↓
Plano de ação
↓
Execução assistida/API/RPA
↓
Logs e relatório final
```

### 3.2 Base bruta imutável

Nunca sobrescrever silenciosamente:

- ID, descrição, data, duração, status, cliente, pasta, tipo/subtipo, executante e vínculo de tarefa originais.

### 3.3 Prioridade de data e duração

Campos prioritários:

- `data_inicio_original`
- `duracao_original`
- `tempo_total_resultante`

### 3.4 Segurança operacional

```text
Modelo interpreta e sugere
Sistema valida
Humano aprova/corrige
Robô executa
Log registra
```

Campos sensíveis exigem validação humana (cliente, pasta, SERV/PROC, data, duração, cobrabilidade, status financeiro, tarefa, criação de hora, status em lote, exclusão/substituição).

---

## 4) Escopo Funcional

### Faz

- Leitura de exportações.
- Limpeza e normalização.
- Geração de links de criação/edição.
- Triagem por IA + validação de schema.
- Geração de workbook de revisão humana.
- Importação de retorno humano.
- Geração de manifest e lotes seguros.
- Execução assistida/automatizada com logs.

### Não faz inicialmente

- Salvar automaticamente no Legal One.
- Alterar campos sensíveis sem confirmação.
- Enviar e-mails automáticos sem revisão.
- Excluir registros.
- Alterar horas lançadas no financeiro.
- Operar sem logs/backup.

---

## 5) Status e Decisões

### Status de foco

- `Pendente`
- `Disponível para aprovação`

### Fluxo especial/auditoria

- `Aprovada`
- `Disponível para financeiro`

### Fora do escopo ordinário

- `Lançada no financeiro` (apenas exceção/auditoria)

### Decisões permitidas

- `APROVAR_SEM_ACAO`
- `CORRIGIR_E_LIBERAR`
- `DEVOLVER_PARA_CORRECAO`
- `REVISAR_HUMANAMENTE`

---

## 6) Arquitetura Técnica Sugerida

```text
robo_legalone/
  README.md
  pyproject.toml | requirements.txt
  .env.example
  .gitignore
  config/
    config.json
    status_map.json
    field_map_legalone.json
    model_prompts/
  data/
    input/
    output/
    logs/
    backups/
  src/
    main.py
    legalone/
    excel/
    model/
    triagem/
    communication/
    audit/
  tests/
```

---

## 7) Configuração de URLs

`config/config.json` (exemplo):

```json
{
  "legalone": {
    "base_url": "https://ballao.novajus.com.br",
    "urls": {
      "criar_hora": "https://ballao.novajus.com.br/TimeSheet/HorasTrabalhadas/CreateHoraTrabalhadaLote?",
      "editar_hora_template": "https://ballao.novajus.com.br/TimeSheet/HorasTrabalhadas/EditHoraTrabalhada/{id_lancamento}?",
      "editar_tarefa_template": null,
      "criar_tarefa_template": null
    }
  },
  "automation": {
    "mode": "dry_run",
    "allow_save": false,
    "require_human_confirmation": true,
    "max_batch_size": 50
  }
}
```

Não inventar templates de tarefa; exigir mapeamento explícito.

---

## 8) Schema Operacional por Lançamento

Cada linha deve gerar objeto com:

- metadados da rodada (`id_rodada`, `data_processamento`, `versao_schema`)
- origem e rastreabilidade (`linha_origem`, `id_lancamento`, `linha_hash`)
- valores originais (status, executante, data/hora/duração, cliente, pasta, tipo, descrição, idioma, cobrabilidade)
- sugestões (cliente/pasta/tipo/idioma/descrição/data/hora/tempo)
- decisão e confiança
- ação sugerida e status destino
- override humano e autorização
- links de execução

---

## 9) Workbook Operacional

Nome sugerido: `LegalOne_Revisao_Horas_[DATA_INICIAL]_[DATA_FINAL]_[ID_RODADA].xlsx`

Abas obrigatórias:

1. `00_README`
2. `01_RAW_LEGALONE`
3. `02_BASE_COMPARATIVA`
4. `03_TRIAGEM_MODELO`
5. `04_REVISAO_HUMANA`
6. `05_PLANO_ACOES_LEGALONE`
7. `06_LOTES_STATUS`
8. `07_CASOS_DUVIDOSOS`
9. `08_LOG_VALIDACOES`
10. `09_RELATORIO_GERENCIAL`
11. `10_MANIFEST_JSON`

Na aba de revisão humana:

- bloquear colunas de origem/rastreabilidade;
- destacar apenas colunas editáveis;
- exigir `autorizar_execucao = SIM` para qualquer execução.

---

## 10) Fluxo Operacional (alto nível)

1. Extrair dados.
2. Salvar bruto imutável.
3. Normalizar.
4. Gerar links.
5. Aplicar regras determinísticas.
6. Enviar para IA.
7. Validar schema da IA.
8. Gerar workbook de revisão.
9. Importar revisão humana.
10. Validar hashes/autorizações.
11. Gerar plano de ações + lotes.
12. Executar conforme modo (`dry_run`, `open_only`, `fill_only`, `fill_and_confirm`, `auto_safe`).
13. Emitir relatório final e logs.

---

## 11) Regras determinísticas pré-IA (mínimo)

- ID vazio → potencial `CREATE_HOUR` + revisão humana.
- Duração vazia/zero → erro crítico.
- Cliente/Pasta vazios → revisão humana.
- Executante vazio → erro crítico.
- Status fora do escopo → bloqueio.
- Cobrável vazio → alerta.
- Descrição/Tipo “DIVERSOS” → alerta.
- Data inválida → erro crítico.

---

## 12) IA: Entrada, Saída e Validação

### Entrada

- payload estruturado com regras de preservação e decisões permitidas.

### Saída obrigatória

- JSON com sugestões, confiança, decisão, justificativa e flags de revisão.

### Validação obrigatória

- JSON válido;
- campos obrigatórios presentes;
- decisão em enum permitido;
- score 0–100;
- consistência confiança/score;
- preservação de data/duração (salvo justificativa);
- baixa confiança implica revisão humana.

Se inválido: logar, tentar reparo e, se necessário, marcar como `REVISAR_HUMANAMENTE`.

---

## 13) Matriz decisão → ação

- `APROVAR_SEM_ACAO` + OK humano → `CHANGE_STATUS`/`CHANGE_STATUS_BULK`
- `CORRIGIR_E_LIBERAR` + OK humano → `UPDATE_HOUR` + `CHANGE_STATUS`
- `DEVOLVER_PARA_CORRECAO` → `RETURN_TO_EXECUTANT`
- `REVISAR_HUMANAMENTE` → `HUMAN_REVIEW_ONLY`
- Override `BLOQUEAR` → `BLOCKED`
- Sem autorização → `NO_ACTION`

Tipos de ação aceitos:

`NO_ACTION`, `UPDATE_HOUR`, `CREATE_HOUR`, `UPDATE_TASK`, `CREATE_TASK`, `CHANGE_STATUS`, `CHANGE_STATUS_BULK`, `RETURN_TO_EXECUTANT`, `HUMAN_REVIEW_ONLY`, `BLOCKED`.

---

## 14) Manifest de Ações

Arquivo base para execução:

- `manifest_acoes_legalone_[id_rodada].json`

Cada ação deve conter:

- identificação (`id_acao`, `id_lancamento`),
- tipo, link de execução,
- status atual/destino,
- valores originais/finais,
- autorização,
- risco,
- confirmação requerida.

---

## 15) Modos de Execução

- `dry_run`: simula sem abrir navegador.
- `open_only`: abre links sem preencher.
- `fill_only`: preenche sem salvar.
- `fill_and_confirm`: preenche e exige confirmação humana.
- `auto_safe`: executa só ações homogêneas, autorizadas e seguras.

Padrão inicial obrigatório: `dry_run`.

---

## 16) Segurança, LGPD e Sigilo

Regras obrigatórias:

- segredos em `.env`;
- não versionar `.env` e dados operacionais;
- mascarar dados sensíveis em logs;
- manter backups e trilha de auditoria;
- registrar rollback por ação.

`.gitignore` deve incluir:

```gitignore
.env
data/input/
data/output/
data/logs/
data/backups/
*.xlsx
*.xlsm
*.csv
*.log
```

---

## 17) Roadmap Incremental (MVPs)

- **MVP 0:** estrutura, config, logger, README.
- **MVP 1:** leitura de Excel + geração de links (ID → URL de edição).
- **MVP 2:** normalização e validações determinísticas.
- **MVP 3:** decisão por regras (sem IA).
- **MVP 4:** integração com IA + validação schema.
- **MVP 5:** workbook de revisão humana (abas e validações).
- **MVP 6:** importação da revisão humana (hash e campos bloqueados).
- **MVP 7:** geração de manifest + lotes.
- **MVP 8:** dry-run completo.
- **MVP 9-11:** RPA progressivo (`open_only` → `fill_only` → `fill_and_confirm`).
- **MVP 12:** execução controlada em lote.

---

## 18) Prompt Inicial Sugerido para Codex/Claude Code

Diretriz inicial de implementação:

1. Criar estrutura Python mínima.
2. Ler planilha de entrada com coluna `ID`.
3. Gerar `link_edicao_hora` por template e `link_criacao_hora` fixo.
4. Salvar planilha de saída.
5. Registrar log.
6. Testar que `ID=1328599` gera:

`https://ballao.novajus.com.br/TimeSheet/HorasTrabalhadas/EditHoraTrabalhada/1328599?`

Não implementar navegador, Playwright, e-mail ou IA na primeira entrega.

---

## 19) Critérios Finais de Sucesso

1. Base bruta preservada.
2. Rastreabilidade por ID/hash.
3. Links corretos por lançamento.
4. Saída de IA validada por schema.
5. Revisão humana com separação de campos bloqueados/editáveis.
6. Override humano preservado.
7. Manifest sem ambiguidade.
8. Distinção correta entre tipos de ação.
9. Lotes homogêneos e autorizados.
10. Nenhum campo sensível alterado sem autorização.
11. Logs completos.
12. Relatório por sucesso/falha/bloqueio.
13. Operação inicia em `dry_run`.
14. Modo assistido antes de automação plena.
15. Financeiro recebe apenas horas validadas/liberadas.

---

## 20) Diretriz Final de Implementação

Ordem correta de evolução:

1. Ler dados.
2. Preservar bruto.
3. Gerar links.
4. Normalizar.
5. Classificar.
6. Gerar planilha.
7. Revisar humanamente.
8. Importar revisão.
9. Gerar manifest.
10. Simular execução.
11. Abrir links.
12. Preencher sem salvar.
13. Preencher com confirmação.
14. Executar em lote apenas o que for seguro.

Essa sequência reduz risco, preserva controle humano e permite evolução modular, testável e reversível.
