# Reconstrutor de Lançamentos do Legal One

Ferramenta CLI em Python que reconstrói, linha a linha, como cada lançamento de horas deveria
ser feito no Legal One. Recebe duas planilhas — uma com lançamentos incompletos do usuário e
uma comparativa com lançamentos bem-feitos da equipe — e produz uma planilha multi-aba pronta
para uso operacional.

## Princípio operacional

**Data de início e duração total são preservadas verbatim.** Esses são os dois dados
prioritários do Legal One; a "Hora de início sugerida" sai sempre como `00:00`, refletindo o
fluxo real (o sistema calcula data/hora final a partir da duração).

## Instalação

```bash
pip install -r requirements.txt
```

## Uso

```bash
python rebuild.py --user A.xlsx --team B.xlsx --out final.xlsx
python rebuild.py --user A.xlsx --team B.xlsx --out final.xlsx --verbose
```

Saída de exemplo:
```
OK  Saída gerada: /caminho/final.xlsx
    Linhas: 10  (alta=0, media=7, baixa=3)
    Revisão humana: 3  Desdobramento sinalizado: 3
```

## Esquema de entrada

Os cabeçalhos são detectados de forma flexível (case-insensitive, sem acentos). Aliases
aceitos estão em `reconstrutor/esquema.py`.

**Arquivo A (usuário) — colunas obrigatórias:**
- Descrição (ou: descricao, atividade, histórico)
- Data início (ou: data, data inicial, início)
- Duração (ou: tempo, tempo total, horas)

Colunas opcionais reconhecidas: hora início, data fim, hora fim, executante, pasta original.

**Arquivo B (equipe) — colunas obrigatórias:**
- Descrição
- Cliente
- Pasta (número da pasta)
- Vínculo (SERV/PROC)

Colunas opcionais reconhecidas: nome da pasta, tipo/subtipo, idioma, executante, data, duração.

## Estrutura da saída (6 abas)

| Aba | Conteúdo |
|---|---|
| `README` | Finalidade, legendas, regra temporal crítica, data de geração. |
| `RAW_USUARIO` | Cópia intacta do Arquivo A. |
| `RAW_EQUIPE` | Cópia intacta do Arquivo B. |
| `SUGESTOES_FINAIS` | 20 colunas operacionais com cliente, vínculo, pasta, descrição reescrita, idioma, confiança. Coloração condicional na coluna de confiança. |
| `CASOS_DUVIDOSOS` | Subset que exige revisão humana (baixa confiança, dúvida SERV/PROC, desdobramento). |
| `PASTAS_REFERENCIADAS` | Pastas da equipe efetivamente consideradas, com frequência, idioma e tipos recorrentes. |

## Regras aplicadas

- **Nunca inventa**: número de pasta, processo, cliente. Quando faltar lastro, marca confiança baixa e pede revisão humana.
- **Vínculo SERV vs PROC**: combina indicadores fortes (parecer, due diligence vs auto de infração, recurso especial, número CNJ) com histórico do cliente como desempate.
- **Idioma**: pasta → cliente → default português, conforme hierarquia da especificação.
- **Descrição**: reescrita no padrão `verbo + objeto + tema + (cliente)`. Sem núcleo identificável, preserva a original e marca baixa confiança.
- **Desdobramento**: linhas com 2+ núcleos ou com `+`/conectores são sinalizadas, mas nunca divididas automaticamente.

## Estrutura do código

```
reconstrutor/
├── esquema.py        # aliases canônicos, enums SERV/PROC, idiomas
├── io_planilhas.py   # leitura xlsx + detecção flexível de colunas
├── normalizar.py     # lower + unidecode + abreviações (só p/ matching)
├── cliente.py        # identificação por sigla, fuzzy, frequência
├── classificar.py    # detecção do núcleo da atividade
├── vinculo.py        # SERV vs PROC com pesos
├── pasta.py          # lookup; nunca inventa
├── tipo_subtipo.py   # tipo mais frequente da pasta
├── idioma.py         # pt/en por hierarquia
├── descricao.py      # reescrita em padrão profissional
├── desdobramento.py  # detecção de múltiplas atividades
├── confianca.py      # alta/média/baixa + revisão humana
├── saida.py          # geração da xlsx multi-aba
└── pipeline.py       # orquestração
```

## Desenvolvimento

```bash
# gerar fixtures sintéticas
python tests/fixtures/gerar_fixtures.py

# rodar testes
python -m pytest tests/ -v

# smoke E2E
python rebuild.py --user tests/fixtures/arquivo_a_demo.xlsx \
                  --team tests/fixtures/arquivo_b_demo.xlsx \
                  --out /tmp/saida.xlsx
```

39 testes unitários e E2E cobrem as regras críticas: preservação de data/duração,
nunca-inventar, idioma por pasta, casos duvidosos, desdobramento.
