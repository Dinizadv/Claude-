---
codigo: POP-TIME-LEGALONE-001
versao: 2.0
data_base: 2026-04-12
proprietario: Coordenação Jurídico-Operacional / Departamento Tributário
dependencias: [PB01, PB02, PB03, PB04, PB05, PB06, PB07]
status: Versão institucional consolidada para circulação interna
fonte: 01_Governanca/01_POP_Gestao_de_Horas_Legal_One_v2_0.pdf
---

# POP - Gestão de Horas no Legal One

**Procedimento Operacional Padrão para lançamento, triagem, revisão, aprovação e disponibilização financeira**

| Campo | Valor |
|---|---|
| Código | POP-TIME-LEGALONE-001 |
| Versão | 2.0 |
| Data-base | 12/04/2026 |
| Proprietário | Coordenação Jurídico-Operacional / Departamento Tributário |
| Dependências principais | PB01, PB02, PB03, PB04, PB05, PB06 e PB07 |
| Status | Versão institucional consolidada para circulação interna |

## Resumo executivo

Este POP consolida o fluxo de ponta a ponta do timesheet do escritório: lançamento primário, triagem técnica, revisão qualificada, aprovação gerencial, disponibilização financeira e auditoria mensal. O objetivo é reduzir perda de tempo faturável, evitar retrabalho, preservar rastreabilidade e separar claramente erros formais, erros materiais e dúvidas que exigem juízo humano.

> **Diretriz central:** o financeiro não deve funcionar como segunda instância revisora. Só deve receber horas tecnicamente maduras e com classificação gerencial final.

## 1. Objetivo

Padronizar o procedimento de controle de horas no Legal One, assegurando qualidade mínima na origem, triagem conservadora, revisão eficiente de exceções, liberação ordenada ao financeiro e produção consistente de relatórios gerenciais.

## 2. Escopo

- Aplica-se ordinariamente às horas em status Pendente e Disponível para aprovação.
- Não integra o fluxo automático padrão de horas já Aprovadas, Disponíveis para financeiro ou Lançadas no financeiro, salvo exceção formal ou auditoria.
- Abrange tanto a revisão operacional quanto a geração de insumos para relatório gerencial.

## 3. Diretrizes obrigatórias

- Base comparativa da equipe é a fonte de prevalência mais forte.
- Data de início e tempo total são prioritários e não devem ser alterados sem lastro objetivo.
- Campo sensível sem lastro suficiente não deve ser preenchido apenas para completar a linha.
- Toda linha de confiança BAIXA deve receber `revisão_humana = SIM`.
- Cobrabilidade original e cobrabilidade gerencial devem permanecer distinguíveis.
- Correção silenciosa de campo sensível é vedada.
- Toda automação deve operar com logs, reversibilidade e validação humana para ações sensíveis.

## 4. Papéis

| Papel | Responsabilidade principal |
|---|---|
| Executante | Lança a hora, corrige devoluções e responde por informações de origem. |
| Camada de triagem | Classifica cada linha, corrige o que for formalmente seguro e registra confiança/decisão. |
| Revisor técnico | Decide casos ambíguos ou materialmente sensíveis. |
| Sócio ou gerente aprovador | Aplica o gate gerencial final quando o escritório optar por essa etapa. |
| Financeiro | Recebe horas fechadas do ponto de vista do conteúdo e executa faturamento sem reabrir o mérito técnico. |

## 5. Fluxo operacional padronizado

| Fase | Conteúdo |
|---|---|
| Fase 1 — Lançamento primário | Registro tempestivo pelo executante, com campos mínimos e descrição inteligível. |
| Fase 2 — Gate mínimo de entrada | Checagem de campos críticos, datas e duração. Falhas retornam ao executante. |
| Fase 3 — Consolidação da base | Extração controlada da base bruta e preparação da rodada. |
| Fase 4 — Triagem técnica | Classificação em `APROVAR_SEM_ACAO`, `CORRIGIR_E_LIBERAR`, `DEVOLVER_PARA_CORRECAO` ou `REVISAR_HUMANAMENTE`. |
| Fase 5 — Revisão qualificada | Análise humana dos casos devolvidos ou ambíguos. |
| Fase 6 — Aprovação gerencial | Gate final, opcional conforme a governança do escritório. |
| Fase 7 — Disponibilização financeira | Envio apenas de horas tecnicamente fechadas e gerencialmente classificadas. |
| Fase 8 — Auditoria mensal | Controle de conformidade, amostragem, indicadores e retroalimentação de regras. |

## 6. Decisões operacionais e efeitos

| Decisão | Quando usar | Status destino sugerido |
|---|---|---|
| `APROVAR_SEM_ACAO` | Alta confiança, sem erro formal/material relevante | Disponível para aprovação ou financeiro |
| `CORRIGIR_E_LIBERAR` | Erro objetivo, seguro e delimitado | Correção registrada + liberação |
| `DEVOLVER_PARA_CORRECAO` | Erro certo em campo sensível ou dependência do responsável | Pendente |
| `REVISAR_HUMANAMENTE` | Ambiguidade relevante, conflito material ou base insuficiente | Pendente / fila interna |

## 7. Campos sensíveis e correções seguras

- **Sensíveis:** cliente, número da pasta, vínculo SERV/PROC, divisão de lançamento, duração materialmente incoerente e classificação com impacto financeiro/gerencial.
- **Mais facilmente corrigíveis com segurança:** idioma, descrição final, observação do revisor, score/confiança, sinalização de desdobramento e ajustes formais de tipo/subtipo quando houver padrão dominante claro.

## 8. Gates de passagem

| Gate | Pergunta de controle |
|---|---|
| Gate 0 — entrada | Há base mínima? Campos críticos não estão vazios? Datas/duração são válidas? |
| Gate 1 — saída da triagem | Toda linha tem decisão, confiança, justificativa curta e status destino? |
| Gate 2 — saída da revisão | Campos sensíveis foram resolvidos ou a linha foi formalmente devolvida? |
| Gate 3 — pré-financeiro | A linha tem classificação gerencial final, coerência com o lote e ausência de pendência técnica? |
| Gate 4 — auditoria | Amostras, KPIs e não conformidades foram registradas? |

## 9. RACI e SLA

O detalhamento completo está no PB06. Como regra geral: executante responde pela origem; triagem responde pela classificação preliminar; revisor responde pelas exceções; sócio/gerente aprova o lote quando o gate for adotado; financeiro responde pelo fechamento após liberação.

| Etapa | SLA |
|---|---|
| Lançamento primário | Até o fim do dia útil da atividade ou até 10h do dia útil seguinte |
| Correção de devolução | Até 1 dia útil após a devolução |
| Triagem inicial | Até 1 dia útil após consolidação da base |
| Revisão humana | Até 2 dias úteis após entrada na fila |
| Aprovação gerencial | Até 1 dia útil após liberação técnica |
| Disponibilização ao financeiro | Até 1 dia útil após aprovação |
| Relatório de auditoria | Até o 5º dia útil do mês subsequente |

## 10. Controles obrigatórios

- **Controle temporal:** data de início e tempo total têm precedência sobre campos acessórios.
- **Controle de idioma:** pasta > cliente > tipo/subtipo > histórico semelhante.
- **Controle de conflito:** conflito entre dois campos sensíveis implica revisão humana.
- **Controle de reclassificação:** divergências entre cobrável original e gerencial devem ser justificadas.
- **Controle de consistência final:** resumo, analítico e composição do tempo devem fechar entre si.

## 11. Auditoria mensal

A auditoria mensal deve cobrir 100% dos casos em revisão humana e devolvidos, 100% das reclassificações de cobrabilidade e amostras mínimas das linhas aprovadas ou corrigidas automaticamente. O protocolo detalhado está no PB07.

- Classificar achados em crítico, alto, médio e baixo.
- Medir taxa de retrabalho, taxa de erro formal, taxa de erro material e tempo médio de ciclo.
- Identificar padrões recorrentes por executante, matéria, cliente ou pasta.
- Retroalimentar thresholds, regras de prudência e treinamento.

## 12. Implantação e evolução

O modelo-alvo é progressivo: primeiro planilha e triagem assistida; depois lotes semiautomáticos; por fim, automação assistida com logs e confirmação humana. Integração direta com API ou RPA somente após amadurecimento dos controles.

> **Ponto de prudência:** não há autorização para automação cega em campo sensível. O projeto foi desenhado em regime human-in-the-loop.

## 13. Documentos vinculados

- **PB01_Prompt_Mestre_v2_0** — Ponto de entrada central para reconstrução, revisão, triagem e classificação operacional.
- **PB02_Checklist_Operacional_v2_0** — Checklist de execução, validação, go/no-go e fechamento de rodada.
- **PB03_Schema_de_Saida_v2_0** — Estrutura canônica dos campos de origem, campos sugeridos, campos decisórios e extensões.
- **PB04_Regras_de_Decisao_v2_0** — Matriz de decisão, confiança, prudência, resolução de conflitos e override humano.
- **PB05_Glossario_Operacional_v2_0** — Definições operacionais do projeto, termos do Legal One, abreviações e status.
- **PB06_Matriz_RACI_SLA_e_Gates_v2_0** — Papéis, responsabilização, gates, escalonamento e prazos por etapa.
- **PB07_Protocolo_de_Auditoria_Mensal_e_KPIs_v2_0** — Critérios de auditoria, amostragem, classificação de achados e indicadores.
- **PB08_Plano_de_Implementacao_e_Rollout_v2_0** — Implantação em fases, riscos, dependências técnicas, treinamento e rollout.
- **PB09_Templates_de_Comunicacao_e_Devolucao_v2_0** — Mensagens-padrão para devolução, pedido de complemento, SLA e liberação.
- **README_Carregamento_de_Contexto_LegalOne_v2_0** — Guia de combinação dos módulos conforme o tipo de pedido futuro.
