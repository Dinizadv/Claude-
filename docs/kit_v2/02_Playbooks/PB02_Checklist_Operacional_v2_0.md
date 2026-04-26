---
codigo: PB02
versao: 2.0
escopo: Checklist de preparação, execução, validação e fechamento
dependencias: [PB01, PB03, PB04, PB05]
uso_tipico: Antes, durante e depois de cada rodada de reconstrução, revisão ou triagem
fonte: 02_Playbooks/PB02_Checklist_Operacional_v2_0.pdf
---

# PB02 - Checklist Operacional

**Execução, validação, go/no-go e fechamento de rodada**

| Campo | Valor |
|---|---|
| Código | PB02 |
| Versão | 2.0 |
| Escopo | Checklist de preparação, execução, validação e fechamento. |
| Dependências | PB01, PB03, PB04 e PB05 |
| Uso típico | Antes, durante e depois de cada rodada de reconstrução, revisão ou triagem |

## 1. Critérios de go/no-go

- A base de entrada possui ao menos 80% dos campos mínimos aplicáveis?
- A base comparativa cobre ao menos 60% dos clientes presentes na base de entrada?
- Os arquivos estão íntegros e legíveis?
- O objetivo da rodada foi explicitamente definido?
- Se a resposta for NÃO em item crítico, registrar risco e decidir se a rodada prossegue com ressalvas ou é devolvida.

## 2. Antes de começar

- Confirmar existência da planilha de entrada e da base comparativa.
- Confirmar objetivo da rodada: reconstrução, revisão, triagem/aprovação ou relatório gerencial.
- Registrar data da rodada, operador responsável e versão do pacote utilizado.

## 3. Higiene e normalização

- Remover separadores redundantes, espaços duplicados e variações irrelevantes de escrita.
- Preservar o conteúdo semântico original.
- Manter cópia íntegra da base bruta.

## 4. Validação formal

- Checar data inválida, duração inválida, cliente vazio, pasta vazia, executante vazio e idioma inconsistente.
- Sinalizar descrição excessivamente telegráfica e conflito entre campos formais.
- Checar sobreposição temporal entre lançamentos do mesmo executante.

## 5. Análise substantiva

- Há lastro suficiente para cliente, natureza e pasta?
- O idioma segue o padrão da pasta/cliente?
- A descrição final está profissional e útil?
- Há base racional para desdobramento?

## 6. Classificação operacional

- Toda linha recebeu recomendação principal, confiança, decisão e justificativa curta?
- Toda linha BAIXA está marcada para revisão humana?

## 7. Consistência da saída

- Não houve inferência fraca apresentada como certeza.
- Alternativas plausíveis foram registradas quando cabível.
- Extensões de triagem e gerencial foram preenchidas quando aplicáveis.

## 8. Controle final

- Resumo e analítico fecham.
- Totais por advogado, cliente e pasta estão coerentes.
- Inconsistências não foram ocultadas.
- Apresentação final é legível, auditável e pronta para circulação interna.

## 9. Métricas mínimas da rodada

| Métrica | Finalidade |
|---|---|
| % linhas ALTA | Percentual de linhas com confiança alta. |
| % linhas BAIXA | Percentual de linhas que exigem revisão humana. |
| % `APROVAR_SEM_ACAO` | Mede estabilidade da base e maturidade do fluxo. |
| % `DEVOLVER_PARA_CORRECAO` | Mede retrabalho na origem. |
| Cobertura da base comparativa | Percentual de linhas com match suficientemente forte. |
| Tempo médio por linha | Apoia dimensionamento operacional da rodada. |

> **Regra final de prudência:** quando houver dúvida real, registrar a alternativa plausível, reduzir a confiança e marcar revisão humana.
