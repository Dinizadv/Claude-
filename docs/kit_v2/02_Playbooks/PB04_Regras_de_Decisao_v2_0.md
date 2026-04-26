---
codigo: PB04
versao: 2.0
escopo: Define a lógica decisória do projeto
dependencias: [PB03, PB05]
uso_tipico: Triagem, revisão, aprovação e automação assistida
fonte: 02_Playbooks/PB04_Regras_de_Decisao_v2_0.pdf
---

# PB04 - Regras de Decisão e Confiança

**Matriz operacional de prudência, thresholds, conflitos e override humano**

| Campo | Valor |
|---|---|
| Código | PB04 |
| Versão | 2.0 |
| Escopo | Define a lógica decisória do projeto. |
| Dependências | PB03 e PB05 |
| Uso típico | Triagem, revisão, aprovação e automação assistida |

## 1. Princípio central

A decisão não avalia apenas se a linha está certa ou errada. Ela deve refletir qualidade do dado, segurança da inferência, impacto operacional da correção e necessidade de intervenção humana.

## 2. As quatro decisões operacionais

| Decisão | Definição operacional |
|---|---|
| `APROVAR_SEM_ACAO` | Sem erro formal ou material relevante; confiança ALTA; sem indício material de desdobramento. |
| `CORRIGIR_E_LIBERAR` | Erro objetivo ou lacuna corrigível com segurança e sem juízo humano sensível. |
| `DEVOLVER_PARA_CORRECAO` | Erro certo em campo sensível ou dependência do responsável. |
| `REVISAR_HUMANAMENTE` | Ambiguidade relevante, conflito material ou confiança BAIXA. |

## 3. Escala de confiança

| Grau | Condições típicas |
|---|---|
| ALTA | Convergência forte entre cliente, matéria, pasta, idioma e padrão histórico. |
| MEDIA | Boa aderência geral com lacuna não crítica ou pequena disputa entre alternativas. |
| BAIXA | Cliente apenas presumido, conflito real entre SERV e PROC, múltiplas pastas fortes ou base comparativa fraca. |

## 4. Thresholds quantitativos sugeridos

| Decisão | Threshold orientativo |
|---|---|
| `APROVAR_SEM_ACAO` | `confianca_score >= 85` e zero conflito em campo sensível |
| `CORRIGIR_E_LIBERAR` | `confianca_score >= 60` e somente campos não sensíveis a corrigir |
| `DEVOLVER_PARA_CORRECAO` | erro demonstrado em campo sensível, independentemente do score |
| `REVISAR_HUMANAMENTE` | `confianca_score < 50` ou conflito sensível não resolvível |

## 5. Regra automática de prudência

Toda linha com confiança BAIXA deve receber `revisao_humana = SIM`, justificativa curta e alternativa plausível, se houver.

## 6. Critérios de campo sensível

- Cliente.
- Número da pasta.
- Vínculo SERV/PROC.
- Classificação de cobrança com impacto gerencial ou financeiro.
- Divisão de lançamento.
- Duração quando houver inconsistência material.

## 7. Resolução de conflitos

- Se dois campos sensíveis conflitam, a decisão padrão é `REVISAR_HUMANAMENTE`.
- Se um campo sensível conflita com um não sensível, prevalece o campo sensível.
- Se a base comparativa conflita com a descrição original, prevalece a base comparativa, salvo prova objetiva em sentido contrário.
- Se o conflito ocorrer apenas entre inferências, registrar ambas as alternativas e reduzir a confiança.

## 8. Override humano e recorrência

- O revisor humano pode sobrescrever a decisão do modelo, desde que registre o motivo.
- Erros recorrentes por executante, cliente ou matéria devem gerar alerta de coaching/processo, não apenas decisão linha a linha.
- A automação não substitui o juízo técnico em hipóteses sensíveis.

> **Regra contra excesso de automação:** o projeto não admite correção silenciosa de campo sensível sem justificativa e sem trilha de auditoria.
