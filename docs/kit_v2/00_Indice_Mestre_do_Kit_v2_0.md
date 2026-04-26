---
codigo: KIT-LEGALONE-2026-V2
versao: 2.0
data_base: 2026-04-12
proprietario: Coordenação Jurídico-Operacional / Departamento Tributário
confidencialidade: Uso interno restrito
fonte: 00_Indice_Mestre_do_Kit_v2_0.pdf
---

# Índice Mestre do Kit Documental

**Projeto Legal One | Gestão de Horas, Triagem, Revisão, Aprovação e Relatório Gerencial**

| Campo | Valor |
|---|---|
| Código do conjunto | KIT-LEGALONE-2026-V2 |
| Versão | 2.0 |
| Data-base | 12/04/2026 |
| Proprietário | Coordenação Jurídico-Operacional / Departamento Tributário |
| Confidencialidade | Uso interno restrito |
| Função | Mapa de navegação, compatibilidade e uso do ecossistema documental consolidado. |

> **Objetivo do índice:** oferecer visão única do sistema documental, indicar o que foi mantido, o que foi absorvido e como cada peça deve ser usada em conjunto.

## 1. Arquitetura do kit

O kit está organizado em quatro camadas complementares: governança normativa, playbooks operacionais, controle e implantação, e contexto de carregamento. O desenho foi construído para reduzir redundância, padronizar terminologia e permitir uso humano e uso assistido por IA no mesmo ecossistema.

- **Camada normativa:** POP e matriz de papéis, gates e SLA.
- **Camada operacional:** prompt mestre, checklist, schema, regras de decisão e glossário.
- **Camada de controle:** protocolo de auditoria, templates de comunicação e plano de implementação.
- **Camada contextual:** README de carregamento e fluxograma do processo.

## 2. Inventário do kit

| Arquivo | Finalidade |
|---|---|
| 00_Indice_Mestre_do_Kit_v2_0 | Mapa do kit, arquitetura documental, compatibilidade com o ecossistema atual e ordem de uso. |
| 01_POP_Gestao_de_Horas_Legal_One_v2_0 | Norma-mãe do procedimento: fluxo, papéis, controles, auditoria, SLA e governança. |
| PB01_Prompt_Mestre_v2_0 | Ponto de entrada central para reconstrução, revisão, triagem e classificação operacional. |
| PB02_Checklist_Operacional_v2_0 | Checklist de execução, validação, go/no-go e fechamento de rodada. |
| PB03_Schema_de_Saida_v2_0 | Estrutura canônica dos campos de origem, campos sugeridos, campos decisórios e extensões. |
| PB04_Regras_de_Decisao_v2_0 | Matriz de decisão, confiança, prudência, resolução de conflitos e override humano. |
| PB05_Glossario_Operacional_v2_0 | Definições operacionais do projeto, termos do Legal One, abreviações e status. |
| PB06_Matriz_RACI_SLA_e_Gates_v2_0 | Papéis, responsabilização, gates, escalonamento e prazos por etapa. |
| PB07_Protocolo_de_Auditoria_Mensal_e_KPIs_v2_0 | Critérios de auditoria, amostragem, classificação de achados e indicadores. |
| PB08_Plano_de_Implementacao_e_Rollout_v2_0 | Implantação em fases, riscos, dependências técnicas, treinamento e rollout. |
| PB09_Templates_de_Comunicacao_e_Devolucao_v2_0 | Mensagens-padrão para devolução, pedido de complemento, SLA e liberação. |
| README_Carregamento_de_Contexto_LegalOne_v2_0 | Guia de combinação dos módulos conforme o tipo de pedido futuro. |

## 3. Matriz de compatibilidade com o ecossistema atual

A tabela a seguir mostra como os documentos já produzidos foram tratados na consolidação da versão 2.0.

| Arquivo anterior | Arquivo/resultado atual | Tratamento |
|---|---|---|
| POP_Gestao_de_Horas_Legal_One_v1_0.docx | 01_POP_Gestao_de_Horas_Legal_One_v2_0 | Revisado, ampliado e convertido em norma-mãe. |
| PB01_Prompt_Mestre.docx | PB01_Prompt_Mestre_v2_0 | Mantido com melhorias de governança, time leakage e LGPD. |
| PB02_Checklist_Operacional.docx | PB02_Checklist_Operacional_v2_0 | Expandido com go/no-go, métricas e consistência temporal. |
| PB03_Schema_Saida.docx | PB03_Schema_de_Saida_v2_0 | Expandido com auditoria temporal, score numérico e hash. |
| PB04_Regras_Decisao.docx | PB04_Regras_de_Decisao_v2_0 | Ampliado com thresholds, conflitos, override e recorrência. |
| PB05_Glossario.docx | PB05_Glossario_Operacional_v2_0 | Ampliado com termos do Legal One, abreviações e exemplos. |
| README_CARREGAMENTO_CONTEXTO_LEGALONE.md | README_Carregamento_de_Contexto_LegalOne_v2_0 | Atualizado para refletir o kit consolidado. |
| Revisao_Detalhada_Pacote_LegalOne.docx | Absorvido transversalmente | Usado como matriz de lacunas e melhorias prioritárias. |
| instrucoes_projeto_legalone_reconstrucao_lancamentos_v2.md | Absorvido transversalmente | Mantido como premissa metodológica do sistema. |
| ABA TAX PROMPT HORAS GERENCIAL.pdf | Absorvido transversalmente | Serviu de base para relatório gerencial e reclassificações. |
| Revisão de Lançamentos Horários.txt | Absorvido transversalmente | Serviu de base para a esteira triagem-revisão-aprovação. |
| Gestão de horas Legal One.txt | Absorvido transversalmente | Serviu de base externa sobre boas práticas e IA no Legal One. |

## 4. Regras de leitura e precedência

- Quando houver conflito entre base comparativa e inferência fraca, prevalece a base comparativa.
- Quando houver conflito entre dois campos sensíveis sem elemento resolutivo, a linha deve ir para revisão humana.
- O kit foi desenhado para permitir uso modular: não é necessário carregar tudo em toda rodada.
- O POP é a norma-mãe; os playbooks detalham execução e decisão; os anexos operacionais dão suporte à implantação e auditoria.

## 5. Combinações recomendadas por tipo de tarefa

| Tipo de tarefa | Combinação mínima recomendada |
|---|---|
| Reconstrução linha a linha | PB01 + PB02 + PB03 + PB04 + PB05 + README |
| Triagem, aprovação e devolução | POP + PB02 + PB03 + PB04 + PB05 + PB06 |
| Relatório gerencial de horas | POP + PB02 + PB03 (extensão gerencial) + PB05 |
| Auditoria mensal | POP + PB06 + PB07 + PB09 |
| Implantação e rollout | POP + PB06 + PB08 + README |

## 6. Principais melhorias incorporadas na versão 2.0

- Cabeçalho padronizado de versionamento, proprietário, escopo e dependências.
- Regras de go/no-go antes da rodada e métricas mínimas de qualidade.
- Campos de auditoria temporal, score numérico de confiança, hash de origem e override humano.
- Resolução de conflitos entre regras, thresholds de decisão e alerta de padrões recorrentes.
- Ampliação do glossário com termos do Legal One, abreviações recorrentes e mapeamento de status.
- Integração explícita entre fluxo operacional, auditoria mensal, implantação e comunicação interna.
