"""Lookup de pastas na base da equipe. Nunca inventa."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field

import pandas as pd
from rapidfuzz import fuzz

from .esquema import IDIOMA_EN, IDIOMA_PT, VINCULO_DUVIDA


@dataclass
class CandidatoPasta:
    numero: str
    nome: str
    cliente: str
    vinculo: str
    freq: int
    idioma: str                       # pt/en predominante na pasta
    tipos_subtipos: list[str] = field(default_factory=list)
    score: float = 0.0


def _detectar_idioma(textos: list[str]) -> str:
    """Heurística simples: presença de stopwords inglesas vs portuguesas."""
    blob = " ".join(t.lower() for t in textos if isinstance(t, str))
    if not blob:
        return IDIOMA_PT
    pt = sum(blob.count(w) for w in [" de ", " do ", " da ", " para ", " com ", " e ", " sobre ", "ção", "ões"])
    en = sum(blob.count(w) for w in [" of ", " the ", " on ", " for ", " with ", " and ", " analysis", " review", " drafting"])
    return IDIOMA_EN if en > pt else IDIOMA_PT


def construir_indice(df_equipe: pd.DataFrame, mapa: dict[str, str]) -> list[CandidatoPasta]:
    """Agrega a base da equipe em candidatos únicos por (cliente, vinculo, numero)."""
    col_cli = mapa["cliente"]
    col_num = mapa["numero_pasta"]
    col_nome = mapa.get("nome_pasta")
    col_vinc = mapa["vinculo"]
    col_tipo = mapa.get("tipo_subtipo")
    col_desc = mapa.get("descricao")

    grupos: dict[tuple[str, str, str], dict] = {}
    for _, row in df_equipe.iterrows():
        cli = str(row.get(col_cli, "")).strip()
        num = str(row.get(col_num, "")).strip()
        vinc = str(row.get(col_vinc, "")).strip().upper()
        if not cli or not num or not vinc:
            continue
        chave = (cli, vinc, num)
        g = grupos.setdefault(chave, {
            "nome": str(row.get(col_nome, "")).strip() if col_nome else "",
            "freq": 0,
            "tipos": Counter(),
            "descricoes": [],
        })
        g["freq"] += 1
        if col_tipo:
            t = row.get(col_tipo)
            if t and not (isinstance(t, float) and pd.isna(t)):
                g["tipos"][str(t).strip()] += 1
        if col_desc:
            d = row.get(col_desc)
            if d and not (isinstance(d, float) and pd.isna(d)):
                g["descricoes"].append(str(d))

    candidatos: list[CandidatoPasta] = []
    for (cli, vinc, num), g in grupos.items():
        idioma = _detectar_idioma(g["descricoes"] + [g["nome"]])
        tipos_ord = [t for t, _ in g["tipos"].most_common()]
        candidatos.append(CandidatoPasta(
            numero=num,
            nome=g["nome"],
            cliente=cli,
            vinculo=vinc,
            freq=g["freq"],
            idioma=idioma,
            tipos_subtipos=tipos_ord,
        ))
    return candidatos


def escolher(
    cliente: str | None,
    vinculo: str,
    descricao_norm: str,
    indice: list[CandidatoPasta],
) -> tuple[CandidatoPasta | None, CandidatoPasta | None]:
    """Retorna (principal, alternativa). Nunca inventa: se nada bater, ambos None.

    Regras (Etapa 6 da spec):
      1. mesmo cliente + mesmo vinculo;
      2. se múltiplos: mais aderente à descrição (fuzzy contra nome da pasta);
      3. desempate por frequência;
      4. registra alternativa se 2º estiver próximo.
    """
    if not cliente or not indice:
        return None, None
    # se vínculo está em dúvida, considera ambos
    if vinculo == VINCULO_DUVIDA:
        candidatos = [c for c in indice if c.cliente == cliente]
    else:
        candidatos = [c for c in indice if c.cliente == cliente and c.vinculo == vinculo]
    if not candidatos:
        # fallback: outras pastas do mesmo cliente em qualquer vínculo
        candidatos = [c for c in indice if c.cliente == cliente]
    if not candidatos:
        return None, None

    for c in candidatos:
        ader = fuzz.partial_ratio(descricao_norm, (c.nome or "").lower()) / 100.0 if descricao_norm and c.nome else 0.0
        c.score = ader * 2.0 + (c.freq / 10.0)

    candidatos.sort(key=lambda c: (c.score, c.freq), reverse=True)
    principal = candidatos[0]
    alternativa = None
    if len(candidatos) > 1:
        segundo = candidatos[1]
        if (principal.score - segundo.score) < 0.5 or segundo.freq >= principal.freq * 0.6:
            alternativa = segundo
    return principal, alternativa
