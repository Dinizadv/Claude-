# README de Carregamento — Kit Legal One v2.0

## Finalidade

Este README define **quais arquivos carregar juntos**, conforme o tipo de solicitação futura, para maximizar reaproveitamento, reduzir redundância e estabilizar o comportamento do modelo.

## Núcleo operacional padrão

Sempre que a tarefa envolver execução prática sobre base de horas, carregar primeiro:

1. `PB01_Prompt_Mestre_v2_0.docx`
2. `PB02_Checklist_Operacional_v2_0.docx`
3. `PB03_Schema_de_Saida_v2_0.docx`
4. `PB04_Regras_de_Decisao_v2_0.docx`
5. `PB05_Glossario_Operacional_v2_0.docx`

## Combinações exatas por tipo de solicitação

### 1. Reconstrução linha a linha
- Obrigatórios: PB01, PB02, PB03, PB04, PB05 e este README.
- Adicionar o POP quando a rodada também exigir governança de status ou liberação ao financeiro.

### 2. Triagem, aprovação, devolução e fluxo de status
- Obrigatórios: POP, PB02, PB03, PB04, PB05 e PB06.

### 3. Revisão de inconsistências e automação assistida
- Obrigatórios: PB01, PB02, PB03, PB04, PB05 e PB06.
- Adicionar PB09 quando a saída incluir comunicação ao executante.

### 4. Relatório gerencial
- Obrigatórios: POP, PB02, PB03 (extensão gerencial) e PB05.
- Adicionar PB07 quando a entrega também incluir auditoria e KPIs.

### 5. Auditoria mensal
- Obrigatórios: POP, PB06, PB07 e PB09.

### 6. Implantação e rollout
- Obrigatórios: POP, PB06, PB08 e este README.

## Ordem recomendada

1. instrução operacional  
2. regra de validação  
3. regra de saída  
4. regra de decisão  
5. glossário  
6. módulo temático específico

## Estrutura do pacote

- `00_Indice_Mestre_do_Kit_v2_0.docx/pdf`
- `01_Governanca/`
- `02_Playbooks/`
- `03_Operacao_Controle/`
- `04_Contexto_Referencia/`
- `05_Fluxos_Anexos/`

## Regra de prudência

Quando houver dúvida real, preferir registrar a alternativa plausível, reduzir a confiança e marcar revisão humana.
