---
codigo: PB06
versao: 2.0
escopo: Suporte operacional ao POP
dependencias: [POP, PB04, PB07]
uso_tipico: Implantação, operação recorrente e governança
fonte: 03_Operacao_Controle/PB06_Matriz_RACI_SLA_e_Gates_v2_0.pdf
---

# PB06 - Matriz RACI, SLA e Gates

**Papéis, prazos, responsabilização, gates e escalonamento do fluxo**

| Campo | Valor |
|---|---|
| Código | PB06 |
| Versão | 2.0 |
| Escopo | Suporte operacional ao POP |
| Dependências | POP, PB04 e PB07 |
| Uso típico | Implantação, operação recorrente e governança |

## 1. Matriz RACI

| Etapa | Executante | Triagem | Revisor | Sócio/Gerente | Financeiro |
|---|---|---|---|---|---|
| Lançamento primário | R | I | I | I | I |
| Gate mínimo de entrada | R | C | I | I | I |
| Consolidação da base | I | R | A | I | I |
| Triagem automática/semiassistida | I | R | A | I | I |
| Correção de devolução | R | I | A | I | I |
| Revisão técnica | C | I | R/A | C | I |
| Aprovação gerencial | I | I | C | R/A | I |
| Disponibilização ao financeiro | I | I | C | A | R |
| Auditoria mensal | I | C | R | A | C |

> Legenda: **R** = Responsável; **A** = Aprovador; **C** = Consultado; **I** = Informado.

## 2. SLA operacional

| Etapa | Prazo | Natureza |
|---|---|---|
| Lançamento primário | Mesmo dia útil / até 10h do dia útil seguinte | Obrigatório |
| Correção de devolução | 1 dia útil | Obrigatório |
| Triagem | 1 dia útil após consolidação | Obrigatório |
| Revisão humana | 2 dias úteis | Obrigatório |
| Aprovação gerencial | 1 dia útil | Condicional ao gate |
| Disponibilização ao financeiro | 1 dia útil | Obrigatório |
| Relatório de auditoria | Até o 5º dia útil do mês subsequente | Obrigatório |

## 3. Gates de processo

| Gate | Momento | Critério de aprovação |
|---|---|---|
| Gate 0 | Entrada | Base mínima íntegra para seguir à triagem |
| Gate 1 | Saída da triagem | Toda linha com decisão, score, confiança, justificativa e destino |
| Gate 2 | Saída da revisão | Campos sensíveis resolvidos ou devolução formalizada |
| Gate 3 | Pré-financeiro | Linha pronta para faturamento, sem pendência técnica |
| Gate 4 | Fechamento mensal | Auditoria emitida e indicadores registrados |

## 4. Escalonamento

- Vencimento de SLA do executante: alerta ao coordenador.
- Vencimento de SLA da revisão: alerta ao sócio/gerente.
- Divergência pré-financeira: retorno obrigatório ao revisor técnico.
- Achado crítico em auditoria: abertura de plano de ação e revisão de regra.
