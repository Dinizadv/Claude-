"""Gera planilhas .xlsx sintéticas para testes do pipeline.

Cobre os 8 casos descritos no plano:
  1. descrição clara → SERV alta confiança;
  2. descrição com nº de processo → PROC alta confiança;
  3. sigla + matéria recorrente → média confiança;
  4. descrição muito telegráfica → baixa, revisão humana;
  5. cliente com 2 pastas plausíveis → registra alternativa;
  6. descrição com '+' e dois verbos → desdobramento sinalizado;
  7. cliente cuja pasta histórica é em inglês → descrição em en;
  8. linha sem cliente identificável → baixa, sem inventar pasta.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


AQUI = Path(__file__).parent
SAIDA_A = AQUI / "arquivo_a_demo.xlsx"
SAIDA_B = AQUI / "arquivo_b_demo.xlsx"


def gerar_arquivo_b() -> pd.DataFrame:
    rows = [
        # POSITIVO — aduaneiro, SERV (3x), pt
        {"Cliente": "POSITIVO", "Pasta": "10001", "Nome pasta": "POSITIVO - ADUANEIRO",
         "Vinculo": "SERV", "Tipo/Subtipo": "Análise de documentos",
         "Descricao": "Análise de documentos sobre matéria aduaneira.",
         "Data": "2025-01-10", "Tempo": "01:00", "Executante": "ADV1", "Idioma": "pt"},
        {"Cliente": "POSITIVO", "Pasta": "10001", "Nome pasta": "POSITIVO - ADUANEIRO",
         "Vinculo": "SERV", "Tipo/Subtipo": "Análise de documentos",
         "Descricao": "Análise de documentos e alinhamento sobre classificação fiscal.",
         "Data": "2025-01-12", "Tempo": "00:45", "Executante": "ADV1", "Idioma": "pt"},
        {"Cliente": "POSITIVO", "Pasta": "10001", "Nome pasta": "POSITIVO - ADUANEIRO",
         "Vinculo": "SERV", "Tipo/Subtipo": "Pesquisa",
         "Descricao": "Pesquisa sobre devolução de mercadorias e creditamento fiscal.",
         "Data": "2025-01-15", "Tempo": "02:00", "Executante": "ADV2", "Idioma": "pt"},
        # POSITIVO — segunda pasta, também SERV, menos frequente
        {"Cliente": "POSITIVO", "Pasta": "10002", "Nome pasta": "POSITIVO - CONSULTIVO TRIBUTARIO",
         "Vinculo": "SERV", "Tipo/Subtipo": "Reunião | interna",
         "Descricao": "Reunião interna para alinhamento sobre creditamento fiscal.",
         "Data": "2025-01-20", "Tempo": "00:30", "Executante": "ADV1", "Idioma": "pt"},

        # SCHAR — PROC (auto de infração), pt
        {"Cliente": "SCHAR", "Pasta": "20001", "Nome pasta": "SCHAR - AUTO INFRACAO CARF",
         "Vinculo": "PROC", "Tipo/Subtipo": "Análise de decisão administrativa",
         "Descricao": "Análise de decisão administrativa do CARF e definição de estratégia recursal.",
         "Data": "2025-02-03", "Tempo": "02:30", "Executante": "ADV3", "Idioma": "pt"},
        {"Cliente": "SCHAR", "Pasta": "20001", "Nome pasta": "SCHAR - AUTO INFRACAO CARF",
         "Vinculo": "PROC", "Tipo/Subtipo": "Petição | elaboração",
         "Descricao": "Elaboração de petição de impugnação a auto de infração.",
         "Data": "2025-02-05", "Tempo": "03:00", "Executante": "ADV3", "Idioma": "pt"},
        # SCHAR — também tem SERV de parecer (minoria)
        {"Cliente": "SCHAR", "Pasta": "20002", "Nome pasta": "SCHAR - PARECER CLASSI FISC",
         "Vinculo": "SERV", "Tipo/Subtipo": "Parecer | revisão, alterações e redação final",
         "Descricao": "Revisão de parecer sobre classificação fiscal de produtos.",
         "Data": "2025-02-10", "Tempo": "01:30", "Executante": "ADV3", "Idioma": "pt"},

        # INPEK — bilíngue mas predominantemente en, SERV
        {"Cliente": "INPEK", "Pasta": "30001", "Nome pasta": "INPEK - INTERNATIONAL TAX",
         "Vinculo": "SERV", "Tipo/Subtipo": "Document | analysis",
         "Descricao": "Analysis of documents and internal discussion regarding customs assessment.",
         "Data": "2025-03-01", "Tempo": "01:15", "Executante": "ADV4", "Idioma": "en"},
        {"Cliente": "INPEK", "Pasta": "30001", "Nome pasta": "INPEK - INTERNATIONAL TAX",
         "Vinculo": "SERV", "Tipo/Subtipo": "Conference Call",
         "Descricao": "Conference call with the client on indirect tax implications.",
         "Data": "2025-03-04", "Tempo": "00:45", "Executante": "ADV4", "Idioma": "en"},
        {"Cliente": "INPEK", "Pasta": "30001", "Nome pasta": "INPEK - INTERNATIONAL TAX",
         "Vinculo": "SERV", "Tipo/Subtipo": "Legal Opinion | review, changes and final wording",
         "Descricao": "Review of legal opinion on tax classification of products.",
         "Data": "2025-03-07", "Tempo": "02:00", "Executante": "ADV4", "Idioma": "en"},

        # AKS — PROC, sustentação oral
        {"Cliente": "AKS", "Pasta": "40001", "Nome pasta": "AKS - RECURSO ESPECIAL STJ",
         "Vinculo": "PROC", "Tipo/Subtipo": "Acompanhamento de julgamento",
         "Descricao": "Preparação para sustentação oral em sessão de julgamento.",
         "Data": "2025-04-02", "Tempo": "04:00", "Executante": "ADV5", "Idioma": "pt"},
        {"Cliente": "AKS", "Pasta": "40001", "Nome pasta": "AKS - RECURSO ESPECIAL STJ",
         "Vinculo": "PROC", "Tipo/Subtipo": "Petição | revisão, alterações e redação final",
         "Descricao": "Revisão de petição de recurso especial.",
         "Data": "2025-04-04", "Tempo": "02:00", "Executante": "ADV5", "Idioma": "pt"},
    ]
    return pd.DataFrame(rows)


def gerar_arquivo_a() -> pd.DataFrame:
    rows = [
        # 1) clara: POSITIVO + classificação fiscal → SERV pasta 10001
        {"Descricao": "POSITIVO - análise de documentos sobre classificação fiscal",
         "Data inicio": "2025-05-02", "Hora inicio": "09:00",
         "Duracao": "01:30", "Executante": "ADV1", "Pasta": "GENERICA"},
        # 2) com número CNJ → PROC
        {"Descricao": "Análise de decisão judicial e diligência - 1234567-89.2024.1.23.4567",
         "Data inicio": "2025-05-03", "Hora inicio": "10:00",
         "Duracao": "02:00", "Executante": "ADV3", "Pasta": "GENERICA"},
        # 3) sigla SCHAR + matéria recorrente, PROC
        {"Descricao": "SCHAR - peticao de impugnacao a auto de infracao",
         "Data inicio": "2025-05-04", "Hora inicio": "11:00",
         "Duracao": "03:00", "Executante": "ADV3", "Pasta": "GENERICA"},
        # 4) telegráfica demais → baixa
        {"Descricao": "ajustes",
         "Data inicio": "2025-05-05", "Hora inicio": "14:00",
         "Duracao": "00:30", "Executante": "ADV1", "Pasta": "GENERICA"},
        # 5) POSITIVO + creditamento → 2 pastas plausíveis (10001 e 10002)
        {"Descricao": "POSITIVO - reuniao interna sobre creditamento fiscal",
         "Data inicio": "2025-05-06", "Hora inicio": "15:00",
         "Duracao": "01:00", "Executante": "ADV1", "Pasta": "GENERICA"},
        # 6) desdobramento: análise + call
        {"Descricao": "POSITIVO - analise de documentos + conference call com cliente",
         "Data inicio": "2025-05-07", "Hora inicio": "09:30",
         "Duracao": "02:00", "Executante": "ADV1", "Pasta": "GENERICA"},
        # 7) INPEK → idioma en, conference call
        {"Descricao": "INPEK - call com cliente sobre indirect tax",
         "Data inicio": "2025-05-08", "Hora inicio": "10:00",
         "Duracao": "00:45", "Executante": "ADV4", "Pasta": "GENERICA"},
        # 8) sem cliente identificável
        {"Descricao": "leitura de jurisprudencia geral",
         "Data inicio": "2025-05-09", "Hora inicio": "16:00",
         "Duracao": "01:00", "Executante": "ADV1", "Pasta": "GENERICA"},
        # 9) AKS sustentação - PROC alta
        {"Descricao": "AKS - preparacao para sustentacao oral",
         "Data inicio": "2025-05-10", "Hora inicio": "08:00",
         "Duracao": "04:00", "Executante": "ADV5", "Pasta": "GENERICA"},
        # 10) SCHAR parecer - SERV
        {"Descricao": "SCHAR parecer classi.fisc. revisao",
         "Data inicio": "2025-05-11", "Hora inicio": "13:00",
         "Duracao": "01:30", "Executante": "ADV3", "Pasta": "GENERICA"},
    ]
    return pd.DataFrame(rows)


def main() -> None:
    AQUI.mkdir(parents=True, exist_ok=True)
    gerar_arquivo_a().to_excel(SAIDA_A, index=False)
    gerar_arquivo_b().to_excel(SAIDA_B, index=False)
    print(f"Gerado: {SAIDA_A}")
    print(f"Gerado: {SAIDA_B}")


if __name__ == "__main__":
    main()
