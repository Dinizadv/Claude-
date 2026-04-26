---
codigo: PB05
versao: 2.0
escopo: Reduz ambiguidades terminológicas do projeto
dependencias: []
uso_tipico: Todas as tarefas com densidade de terminologia interna
fonte: 02_Playbooks/PB05_Glossario_Operacional_v2_0.pdf
---

# PB05 - Glossário Operacional

**Termos do projeto, do Legal One, do timesheet e das categorias gerenciais**

| Campo | Valor |
|---|---|
| Código | PB05 |
| Versão | 2.0 |
| Escopo | Reduz ambiguidades terminológicas do projeto. |
| Dependências | Nenhuma; documento de apoio terminológico. |
| Uso típico | Todas as tarefas com densidade de terminologia interna |

## 1. Termos estruturais

| Termo | Definição |
|---|---|
| Lançamento | Registro individual de hora trabalhada. |
| Linha de origem | Linha da base bruta correspondente ao lançamento exportado. |
| Base comparativa | Planilha da equipe com lançamentos mais completos ou aderentes ao padrão. |
| Recomendação principal | Sugestão central do projeto para a linha. |
| Hipótese controlada | Inferência admissível, desde que não apresentada como certeza. |

## 2. Termos do Legal One

| Termo | Definição |
|---|---|
| SERV | Pasta consultiva, preventiva, opinativa, contratual, documental ou estratégica, sem vínculo processual específico. |
| PROC | Pasta processual ou contenciosa, judicial ou administrativa. |
| Pasta | Unidade operacional do trabalho no sistema. |
| Negociação | Unidade de cobrança vinculada a contrato de honorários. |
| Contrato de honorários | Base contratual que orienta cobrança e faturamento. |
| Workflow | Fluxo automatizado de etapas no sistema. |
| GED | Gerenciamento eletrônico de documentos integrado. |
| Tabela de valores | Tabela de preços por tipo de executante no módulo Time Sheet. |
| Tipo de executante | Classificação do profissional que afeta valor-hora. |
| Hora inicial sugerida | Horário operacional recomendado; pode ser `00:00` conforme o fluxo real. |
| Tempo total | Duração integral da atividade; dado prioritário. |

## 3. Decisões e confiança

| Termo | Definição |
|---|---|
| `APROVAR_SEM_ACAO` | Linha apta a seguir sem mudança de conteúdo. |
| `CORRIGIR_E_LIBERAR` | Linha com erro ou lacuna objetiva, mas corrigível com segurança. |
| `DEVOLVER_PARA_CORRECAO` | Linha com erro certo em campo sensível ou dependência do responsável. |
| `REVISAR_HUMANAMENTE` | Linha com ambiguidade relevante ou baixa confiança. |
| Grau de confiança | ALTA, MEDIA ou BAIXA. |
| Desdobramento | Hipótese de múltiplos núcleos autônomos na mesma linha. |

## 4. Status operacionais

| Status | Definição |
|---|---|
| Pendente | Linha aberta, com erro, dúvida relevante ou dependência de correção. |
| Disponível para aprovação | Linha tecnicamente madura para crivo final. |
| Aprovada | Linha validada formalmente pela governança interna. |
| Disponível para financeiro | Linha fechada do ponto de vista do conteúdo. |
| Lançada no financeiro | Linha fora do escopo ordinário da triagem. |

## 5. Campos de timesheet

| Campo | Definição |
|---|---|
| `OBSERVAÇÕES REVISOR` | Campo textual para diagnóstico e orientação. |
| `CHK_OBS` | Campo auxiliar de verificação. |
| `ID_RPH` | Marcador relacionado ao responsável/tipo de contratação. |
| `ID_NEG` | Campo auxiliar de negociação, inclusive para idioma. |
| `ID_TIPO` | Campo auxiliar ligado ao tipo do lançamento. |
| `IDIOMAS` | Resultado da checagem de idioma: OK ou NOK. |
| `HORAS` | Tempo calculado ou exibido na planilha. |
| `OK FINAL` | Resultado final da revisão. |
| `HIPERLINK` | Link para o registro correspondente no sistema, quando disponível. |

## 6. Abreviações recorrentes

| Abreviação | Sentido operacional |
|---|---|
| AI | Auto de infração |
| PAF | Processo administrativo fiscal |
| EF | Execução fiscal |
| PJ | Processo judicial |
| RJ | Recuperação judicial |
| CF | Classificação fiscal |
| NC | Não cobrável |
| RPH | Marcador relacionado à responsabilidade/tipo de contratação |

> **Regra de leitura:** quando um termo admitir mais de uma acepção possível, prevalece a acepção operacional aqui definida, salvo se o pedido futuro estabelecer expressamente outro sentido.
