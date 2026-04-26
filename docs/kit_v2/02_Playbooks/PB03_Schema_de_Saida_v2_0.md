---
codigo: PB03
versao: 2.0
escopo: Define o formato estável de saída tabular e auditável
dependencias: [PB04, PB05]
uso_tipico: Planilha operacional, revisão humana, automação posterior e relatório gerencial
fonte: 02_Playbooks/PB03_Schema_de_Saida_v2_0.pdf
---

# PB03 - Schema de Saída

**Estrutura canônica dos campos e valores permitidos do projeto**

| Campo | Valor |
|---|---|
| Código | PB03 |
| Versão | 2.0 |
| Escopo | Define o formato estável de saída tabular e auditável. |
| Dependências | PB04 e PB05 |
| Uso típico | Planilha operacional, revisão humana, automação posterior e relatório gerencial |

## 1. Princípios

- Cada linha representa um lançamento de origem.
- Cada linha deve receber uma recomendação principal.
- Dado confirmado deve ser distinguido de inferência.
- Campo sensível sem lastro suficiente deve ficar vazio ou marcado para revisão humana.

## 2. Bloco A — Campos de origem

| Campo | Descrição |
|---|---|
| `linha_origem` | Referência da linha na base bruta |
| `id_lancamento` | Identificador do lançamento |
| `executante` | Profissional responsável |
| `data_inicio_original` | Data original |
| `hora_inicio_original` | Hora original |
| `duracao_original` | Duração integral |
| `cliente_original` | Cliente conforme base |
| `pasta_original` | Número da pasta |
| `nome_pasta_original` | Denominação da pasta |
| `tipo_subtipo_original` | Classificação original |
| `descricao_original` | Texto original |
| `idioma_original` | Idioma original |
| `cobravel_original` | Indicação de cobrabilidade |

## 3. Bloco B — Campos sugeridos

| Campo | Descrição |
|---|---|
| `cliente_sugerido` | Cliente recomendado |
| `vinculo_sugerido` | SERV, PROC ou vazio |
| `numero_pasta_sugerido` | Pasta recomendada |
| `nome_pasta_sugerido` | Nome da pasta recomendada |
| `tipo_subtipo_sugerido` | Tipo/subtipo recomendado |
| `idioma_sugerido` | Idioma recomendado |
| `descricao_sugerida_final` | Descrição profissional reescrita |
| `data_inicio_sugerida` | Data preservada ou ajustada |
| `hora_inicio_sugerida` | Hora inicial recomendada |
| `tempo_total_resultante` | Duração final resultante |
| `duracao_decimal` | Duração em horas decimais para uso gerencial/financeiro |

## 4. Bloco C — Campos decisórios

| Campo | Descrição |
|---|---|
| `confianca_score` | Score numérico de 0 a 100 |
| `grau_confianca` | ALTA, MEDIA ou BAIXA |
| `decisao_modelo` | Uma das quatro decisões operacionais |
| `revisao_humana` | SIM ou NAO |
| `desdobramento` | SIM, NAO ou POSSIVEL |
| `justificativa_curta` | Razão principal da decisão |
| `motivo_principal` | Diagnóstico resumido |
| `base_comparativa_principal` | Referência central usada |
| `alternativa_plausivel` | Segunda opção quando houver |
| `observacoes` | Notas complementares |
| `decisao_humana_override` | SIM ou NAO |
| `motivo_override` | Razão do override humano |

## 5. Bloco D — Auditoria temporal e rastreabilidade

| Campo | Descrição |
|---|---|
| `data_processamento` | Timestamp da rodada |
| `versao_schema` | Versão do schema aplicada |
| `id_rodada` | Identificador único da rodada |
| `linha_hash` | Hash da linha original para deduplicação |
| `operador_rodada` | Responsável pela execução |
| `alerta_recorrencia` | SIM ou NAO para erro recorrente |

## 6. Bloco E — Extensões

| Campo | Descrição |
|---|---|
| `status_atual_legalone` | Status atual no sistema |
| `acao_sistema_sugerida` | Ação recomendada |
| `status_destino_sugerido` | Status-alvo |
| `apto_autoajuste` | Pode ser ajustado automaticamente? |
| `apto_autoliberacao` | Pode ser liberado automaticamente? |
| `motivo_bloqueio` | Razão do impedimento |
| `natureza_pasta` | Processual, Consultivo ou Não classificado |
| `cobrabilidade_original` | Classificação da base |
| `cobrabilidade_gerencial` | Classificação ajustada |
| `categoria_gerencial_tempo` | Categoria A-F |
| `motivo_reclassificacao` | Razão da divergência |

## 7. Valores permitidos e regras de preenchimento

- `vinculo_sugerido`: SERV, PROC ou vazio.
- `grau_confianca`: ALTA, MEDIA ou BAIXA, derivado do `confianca_score`.
- `decisao_modelo`: `APROVAR_SEM_ACAO`, `CORRIGIR_E_LIBERAR`, `DEVOLVER_PARA_CORRECAO` ou `REVISAR_HUMANAMENTE`.
- Não preencher campo sensível apenas para completar a tabela.
- Toda linha deve conter, no mínimo, `descricao_original`, `duracao_original` (se existir), `executante` (se existir), `grau_confianca`, `decisao_modelo`, `revisao_humana` e `justificativa_curta`.
