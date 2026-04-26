"""Decisão entre SERV (consultivo/preventivo) e PROC (contencioso)."""

from __future__ import annotations

import re
from dataclasses import dataclass

import pandas as pd

from .esquema import VINCULO_DUVIDA, VINCULO_PROC, VINCULO_SERV


# Listas extraídas da especificação (Etapa 5). Texto já normalizado.
# Peso 2.0: indicadores fortes/discriminantes. Peso 1.0: indicadores genéricos.
PALAVRAS_SERV: list[tuple[str, float]] = [
    ("parecer", 2.0), ("due diligence", 2.0), ("drafting opinion", 2.0),
    ("opinion", 2.0), ("consultoria", 2.0), ("contratual", 2.0),
    ("review of legal opinion", 2.0), ("minuta de parecer", 2.0),
    ("consultivo", 1.0), ("preventivo", 1.0), ("opinativo", 1.0),
    ("documental", 1.0), ("pesquisa", 1.0), ("entendimento interno", 1.0),
    ("correspondencia", 1.0), ("reuniao", 1.0), ("call", 1.0),
    ("alinhamento interno", 1.0),
]

PALAVRAS_PROC: list[tuple[str, float]] = [
    ("auto de infracao", 2.0), ("execucao fiscal", 2.0), ("agravo", 2.0),
    ("recurso especial", 2.0), ("recurso extraordinario", 2.0),
    ("acao anulatoria", 2.0), ("cumprimento de sentenca", 2.0),
    ("impugnacao", 2.0), ("sessao de julgamento", 2.0),
    ("manifestacao processual", 2.0), ("peticao", 2.0), ("pleading", 2.0),
    ("judgment session", 2.0), ("embargos", 2.0), ("mandado de seguranca", 2.0),
    ("acordao", 2.0), ("sentenca", 2.0), ("decisao judicial", 2.0),
    ("decisao administrativa", 2.0), ("carf", 1.5), ("tribunal", 1.0),
    ("diligencia", 1.0), ("andamento processual", 1.0),
]

# Regex de número CNJ (formato unificado), forte indício de PROC.
RE_NUMERO_PROCESSO = re.compile(r"\b\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}\b")
# Regex genérica de número que parece processual.
RE_NUM_GENERICO = re.compile(r"\b\d{4,}\b")


@dataclass
class DecisaoVinculo:
    vinculo: str             # SERV, PROC ou DUVIDA
    score_serv: float
    score_proc: float
    indicios: list[str]
    alternativa: str | None  # se DUVIDA, qual outro lado quase venceu


def _historico_predominante(cliente: str | None, indice_equipe: pd.DataFrame, mapa: dict[str, str]) -> str | None:
    """Predominância SERV/PROC histórica do cliente na base da equipe."""
    if not cliente or indice_equipe is None or indice_equipe.empty:
        return None
    col_cli = mapa.get("cliente")
    col_vinc = mapa.get("vinculo")
    if not col_cli or not col_vinc:
        return None
    sub = indice_equipe[indice_equipe[col_cli].astype(str).str.strip() == cliente]
    if sub.empty:
        return None
    counts = sub[col_vinc].astype(str).str.upper().str.strip().value_counts()
    if counts.empty:
        return None
    top = counts.index[0]
    if top in (VINCULO_SERV, VINCULO_PROC) and counts.iloc[0] > counts.iloc[1:].sum():
        return top
    return None


def decidir(
    descricao_norm: str,
    cliente: str | None,
    df_equipe: pd.DataFrame,
    mapa_equipe: dict[str, str],
) -> DecisaoVinculo:
    score_serv = 0.0
    score_proc = 0.0
    indicios: list[str] = []

    for p, peso in PALAVRAS_SERV:
        if p in descricao_norm:
            score_serv += peso
            indicios.append(f"serv:{p}")

    for p, peso in PALAVRAS_PROC:
        if p in descricao_norm:
            score_proc += peso
            indicios.append(f"proc:{p}")

    if RE_NUMERO_PROCESSO.search(descricao_norm):
        score_proc += 3.0
        indicios.append("proc:numero_cnj")

    # Histórico do cliente entra como desempate suave (não domina indicadores explícitos).
    pred = _historico_predominante(cliente, df_equipe, mapa_equipe)
    if pred == VINCULO_SERV:
        score_serv += 1.0
        indicios.append("hist_cliente:serv")
    elif pred == VINCULO_PROC:
        score_proc += 1.0
        indicios.append("hist_cliente:proc")

    if score_serv == 0 and score_proc == 0:
        # nenhum sinal: default conservador a SERV (consultivo é o caso geral)
        return DecisaoVinculo(
            vinculo=VINCULO_DUVIDA,
            score_serv=0,
            score_proc=0,
            indicios=["sem_sinais"],
            alternativa=None,
        )

    diff = abs(score_serv - score_proc)
    if diff < 1.0:
        vencedor = VINCULO_SERV if score_serv >= score_proc else VINCULO_PROC
        alt = VINCULO_PROC if vencedor == VINCULO_SERV else VINCULO_SERV
        return DecisaoVinculo(
            vinculo=VINCULO_DUVIDA,
            score_serv=score_serv,
            score_proc=score_proc,
            indicios=indicios + [f"empate:{vencedor}_vs_{alt}"],
            alternativa=alt,
        )

    if score_serv > score_proc:
        return DecisaoVinculo(VINCULO_SERV, score_serv, score_proc, indicios, None)
    return DecisaoVinculo(VINCULO_PROC, score_serv, score_proc, indicios, None)
