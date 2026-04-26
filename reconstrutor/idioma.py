"""Decisão de idioma (pt/en) seguindo a hierarquia da Etapa 9 da spec."""

from __future__ import annotations

import pandas as pd

from .esquema import IDIOMA_EN, IDIOMA_PT
from .pasta import CandidatoPasta


def _detectar(blob: str) -> str:
    blob = blob.lower()
    pt = sum(blob.count(w) for w in [" de ", " do ", " da ", " para ", " com ", " e ", " sobre ", "ção", "ões"])
    en = sum(blob.count(w) for w in [" of ", " the ", " on ", " for ", " with ", " and ", " analysis", " review", " drafting"])
    return IDIOMA_EN if en > pt else IDIOMA_PT


def detectar(
    pasta: CandidatoPasta | None,
    cliente: str | None,
    df_equipe: pd.DataFrame,
    mapa_equipe: dict[str, str],
) -> str:
    """Aplica a hierarquia: pasta -> cliente -> default pt."""
    if pasta is not None:
        return pasta.idioma

    if cliente and not df_equipe.empty:
        col_cli = mapa_equipe.get("cliente")
        col_lang = mapa_equipe.get("idioma")
        col_desc = mapa_equipe.get("descricao")
        sub = df_equipe[df_equipe[col_cli].astype(str).str.strip() == cliente] if col_cli else df_equipe
        if not sub.empty and col_lang and sub[col_lang].notna().any():
            top = sub[col_lang].dropna().astype(str).str.lower().str.strip().value_counts()
            if not top.empty and top.index[0] in (IDIOMA_PT, IDIOMA_EN):
                return top.index[0]
        if not sub.empty and col_desc:
            return _detectar(" ".join(sub[col_desc].dropna().astype(str).tolist()))

    return IDIOMA_PT
