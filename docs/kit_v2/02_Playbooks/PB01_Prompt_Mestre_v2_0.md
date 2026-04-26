---
codigo: PB01
versao: 2.0
escopo: Ponto de entrada central do pacote operacional
dependencias: [PB03, PB04, PB05]
uso_tipico: Reconstrução linha a linha, revisão, triagem e apoio ao relatório gerencial
fonte: 02_Playbooks/PB01_Prompt_Mestre_v2_0.pdf
---

# PB01 - Prompt Mestre

**Reconstrução, revisão operacional, triagem e classificação de lançamentos**

| Campo | Valor |
|---|---|
| Código | PB01 |
| Versão | 2.0 |
| Escopo | Ponto de entrada central do pacote operacional. |
| Dependências | PB03, PB04 e PB05 |
| Uso típico | Reconstrução linha a linha, revisão, triagem e apoio ao relatório gerencial |

## 1. Finalidade

Este playbook define a forma de pensar a linha de timesheet. Ele organiza a hierarquia de fontes, as regras invariantes, o fluxo de análise por passo e o padrão mínimo de recomendação por linha.

## 2. Hierarquia de fontes

| Nível | Fonte | Regra de uso |
|---|---|---|
| 1 | Base comparativa da equipe | Fonte mais forte; prevalece em caso de conflito. |
| 2 | Planilha bruta do usuário | Fonte de origem do lançamento. |
| 3 | Saídas anteriores validadas | Servem como referência estável de comportamento. |
| 4 | Regras operacionais estáveis do acervo | Premissas constantes do projeto. |
| 5 | Hipóteses controladas | Admissíveis apenas quando documentadas como hipótese. |

## 3. Regras invariantes

- Não inventar cliente, número de pasta, processo ou conclusão categórica sem lastro.
- Cada linha recebe uma recomendação principal; não gerar SERV e PROC simultaneamente salvo dúvida real documentada.
- Preservar prioritariamente data de início e duração total.
- A hora inicial pode ser sugerida como `00:00` quando compatível com o fluxo operacional do Legal One.
- Similaridade textual isolada não basta; avaliar cliente, matéria, pasta, idioma e recorrência em conjunto.
- Baixa confiança, ambiguidade material ou indício de desdobramento exigem revisão humana.
- A saída deve distinguir dado confirmado, inferência forte e hipótese controlada.
- Descrições sugeridas devem excluir dados pessoais desnecessários e evitar exposição indevida de informações sensíveis.

## 4. Objetivo por linha

- Cliente sugerido.
- Vínculo principal SERV ou PROC.
- Número e nome da pasta.
- Tipo/subtipo.
- Idioma adequado.
- Descrição final reescrita em padrão profissional.
- Data de início preservada, hora inicial sugerida e duração total preservada.
- Grau de confiança, decisão operacional, revisão humana e base comparativa principal.

## 5. Fluxo de análise em 12 passos

| Passo | Conteúdo |
|---|---|
| Passo 1 | Ler e validar a base de entrada. |
| Passo 1-A | Detectar time leakage: dias sem lançamento, totais diários muito baixos e gaps superiores a 3 horas. |
| Passo 2 | Normalizar os dados para comparação. |
| Passo 3 | Identificar cliente provável. |
| Passo 4 | Identificar natureza da atividade. |
| Passo 5 | Definir SERV ou PROC. |
| Passo 6 | Localizar a pasta correta. |
| Passo 7 | Sugerir tipo/subtipo real do sistema. |
| Passo 8 | Tratar o idioma segundo a ordem de prevalência. |
| Passo 9 | Reescrever a descrição final. |
| Passo 10 | Verificar desdobramento. |
| Passo 11 | Classificar confiança, decisão e necessidade de revisão humana. |
| Passo 12 | Preparar extensão gerencial quando a tarefa também exigir relatório de horas. |

## 6. Casos-limite SERV/PROC

| Exemplo | Classificação principal |
|---|---|
| Pesquisa jurisprudencial para parecer consultivo | SERV |
| Pesquisa jurisprudencial para petição em processo judicial | PROC |
| Reunião interna de estratégia para defesa em auto de infração | PROC |
| Reunião com cliente sobre planejamento tributário | SERV |
| Análise de decisão judicial + orientação ao cliente | Depende: PROC se vinculada a manifestação processual; SERV se apenas informativa |

## 7. Regras adicionais de prudência

- Se o lançamento original estiver em inglês e a pasta for predominantemente em inglês, a descrição final deve permanecer em inglês.
- Quando a duração não estiver em incremento jurídico padrão, preservar a duração original e apenas sinalizar o ponto para regra financeira posterior.
- Se houver mais de uma solução plausível sem dominante forte, registrar a alternativa e reduzir a confiança.
- Se houver conflito entre descrição, base comparativa e pasta histórica, encaminhar a resolução pela matriz do PB04.
