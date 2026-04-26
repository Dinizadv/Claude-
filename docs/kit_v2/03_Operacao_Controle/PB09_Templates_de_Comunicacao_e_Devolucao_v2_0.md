---
codigo: PB09
versao: 2.0
escopo: Padroniza a comunicação operacional do processo
dependencias: [POP, PB06, PB07]
uso_tipico: Devolução ao executante, pedido de complemento, alertas e confirmações
fonte: 03_Operacao_Controle/PB09_Templates_de_Comunicacao_e_Devolucao_v2_0.pdf
---

# PB09 - Templates de Comunicação e Devolução

**Mensagens-padrão do fluxo de correção, revisão, SLA e liberação**

| Campo | Valor |
|---|---|
| Código | PB09 |
| Versão | 2.0 |
| Escopo | Padroniza a comunicação operacional do processo. |
| Dependências | POP, PB06 e PB07 |
| Uso típico | Devolução ao executante, pedido de complemento, alertas e confirmações |

## 1. Modelos de mensagem

### Devolução para correção

> **Assunto:** Ajuste de lançamento de horas - `[cliente/pasta]`
>
> Identificamos inconsistência no lançamento do dia `[data]`. Motivo principal: `[motivo]`.
>
> Providência solicitada: `[ação objetiva]`.
> Prazo: `[SLA]`.
>
> Após o ajuste, a linha retornará para nova triagem.
>
> Coordenação de Horas

### Pedido de complemento

> **Assunto:** Complemento de informação - `[cliente/pasta]`
>
> O lançamento possui base insuficiente para definição segura de `[campo]`. Favor complementar: `[informação necessária]`.
>
> Prazo: `[SLA]`.

### Alerta de SLA

> **Assunto:** SLA próximo do vencimento - revisão de horas
>
> Há linha(s) pendente(s) de sua atuação com vencimento em `[data/hora]`. Favor priorizar o tratamento para evitar impacto no fechamento.

### Confirmação de liberação

> **Assunto:** Horas liberadas para próxima etapa
>
> As linhas do lote `[id]` foram validadas e seguem para `[aprovação/financeiro]`. Não há providência adicional neste momento.

### Registro de achado crítico

> **Assunto:** Achado crítico em auditoria mensal
>
> Foi identificado achado classificado como CRÍTICO no lote `[id]`. Será aberto plano de ação corretivo com responsáveis e prazos.

## 2. Regras de uso

- Mensagens devem ser objetivas, rastreáveis e sem reabrir debate técnico já decidido.
- Não expor informação sensível além do necessário ao ajuste.
- Sempre indicar motivo, providência, prazo e instância responsável.
- Quando houver múltiplas linhas correlatas, preferir comunicação agregada por grupo.
