# Kit Legal One v2.0 — Espelho em Markdown

Transcrição versionada do **Kit Documental v2.0** do projeto Legal One do
Departamento Tributário do Andersen Ballão Advocacia. O conteúdo prescritivo
original está em DOCX/PDF; este diretório espelha cada peça em Markdown para
permitir versionamento, diff via PR, busca textual e ingestão por LLM.

## ⚠️ Alerta de confidencialidade

O cabeçalho de cada peça do Kit indica **`Confidencialidade: Uso interno restrito`**.
Mantenha este repositório (`dinizadv/claude-`) com **visibilidade privada** no
GitHub. **Recomenda-se também tornar privado o repositório de origem
`Dinizadv/Automa-o-Horas-Legal-One`**, do qual o Kit foi baixado.

Se este repositório voltar a ser público, remova `docs/kit_v2/` ou substitua o
conteúdo por placeholders antes do push.

## Provenance

| Campo | Valor |
|---|---|
| Origem | `https://github.com/Dinizadv/Automa-o-Horas-Legal-One/raw/main/Kit_LegalOne_v2_0.zip` |
| Branch / commit do zip | `main` (snapshot acessado em 26/04/2026) |
| Tamanho | 1.081.529 bytes |
| SHA-256 | `076e4d35790451f3c750b67cdb5efcea7d59cda0008fc0c6a4f2c10b440d344b` |
| Conteúdo do zip | 30 arquivos (DOCX + PDF + MD + MMD + PNG + SVG + MANIFEST) |
| Data-base do Kit | 12/04/2026 |
| Código do conjunto | `KIT-LEGALONE-2026-V2` |
| Versão | 2.0 |
| Proprietário | Coordenação Jurídico-Operacional / Departamento Tributário |

### Política de transcrição

- **Fonte canônica:** PDFs do Kit (DOCX é redundante — mesmo conteúdo, mesma data).
- **Motor:** leitura assistida e curadoria manual mínima (cabeçalhos, listas, tabelas GFM, blocos de citação).
- **Sem reescrita semântica.** Onde a transcrição diverge da fonte, prevalece o PDF original (versionado neste mesmo diretório).
- **Markdown e Mermaid pré-existentes** no zip foram copiados literalmente.
- **DOCX não foi replicado** (PDF é equivalente, mais legível e mais leve).

## Estrutura

```
docs/kit_v2/
├── README.md                                 ← este arquivo
├── MANIFEST.txt                              ← lista original do zip
├── 00_Indice_Mestre_do_Kit_v2_0.md   + .pdf
├── 01_Governanca/
│   └── 01_POP_Gestao_de_Horas_Legal_One_v2_0.md   + .pdf
├── 02_Playbooks/
│   ├── PB01_Prompt_Mestre_v2_0.md   + .pdf
│   ├── PB02_Checklist_Operacional_v2_0.md   + .pdf
│   ├── PB03_Schema_de_Saida_v2_0.md   + .pdf
│   ├── PB04_Regras_de_Decisao_v2_0.md   + .pdf
│   └── PB05_Glossario_Operacional_v2_0.md   + .pdf
├── 03_Operacao_Controle/
│   ├── PB06_Matriz_RACI_SLA_e_Gates_v2_0.md   + .pdf
│   ├── PB07_Protocolo_de_Auditoria_Mensal_e_KPIs_v2_0.md   + .pdf
│   ├── PB08_Plano_de_Implementacao_e_Rollout_v2_0.md   + .pdf
│   └── PB09_Templates_de_Comunicacao_e_Devolucao_v2_0.md   + .pdf
├── 04_Contexto_Referencia/
│   ├── Base_de_Consolidacao_do_Kit_v2_0.md
│   ├── README_Carregamento_de_Contexto_LegalOne_v2_0.md
│   └── README_Carregamento_de_Contexto_LegalOne_v2_0.pdf
└── 05_Fluxos_Anexos/
    ├── ANEXO_Fluxograma_Timesheet_v2_0.mmd
    ├── ANEXO_Fluxograma_Timesheet_v2_0.png
    └── ANEXO_Fluxograma_Timesheet_v2_0.svg
```

## Combinações de leitura por tipo de tarefa

Reproduzido do `04_Contexto_Referencia/README_Carregamento_de_Contexto_LegalOne_v2_0.md`:

| Tarefa | Leitura mínima |
|---|---|
| Reconstrução linha a linha | PB01 + PB02 + PB03 + PB04 + PB05 + README de carregamento |
| Triagem, aprovação e devolução | POP + PB02 + PB03 + PB04 + PB05 + PB06 |
| Relatório gerencial de horas | POP + PB02 + PB03 (extensão gerencial) + PB05 |
| Auditoria mensal | POP + PB06 + PB07 + PB09 |
| Implantação e rollout | POP + PB06 + PB08 + README de carregamento |

> **Regra de prudência:** quando houver dúvida real, registrar a alternativa
> plausível, reduzir a confiança e marcar revisão humana.

## Relação com o robô local

O diretório irmão `legalone_robot_v1/` contém um robô determinístico Selenium
para a **Fase 1 (lançamento primário)** do POP. Ele ainda não consome o schema
canônico do PB03 nem o vocabulário decisório do PB04 — ver
`/root/.claude/plans/tente-de-volta-snoopy-storm.md` para o gap-analysis e o
caminho de convergência sugerido.
