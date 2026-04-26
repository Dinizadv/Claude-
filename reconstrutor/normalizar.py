"""Normalização textual usada apenas para matching."""

from __future__ import annotations

import re

import pandas as pd
from unidecode import unidecode


# Abreviações comuns observadas em lançamentos de horas. Usadas só na forma normalizada;
# a descrição original é preservada intacta.
ABREVIACOES = [
    (r"\bclassi\.?\s*fisc\.?\b", "classificacao fiscal"),
    (r"\banal\.?\b", "analise"),
    (r"\bdoc\.?s?\b", "documentos"),
    (r"\breun\.?\b", "reuniao"),
    (r"\bpet\.?\b", "peticao"),
    (r"\brec\.?\b", "recurso"),
    (r"\badm\.?\b", "administrativo"),
    (r"\bjud\.?\b", "judicial"),
    (r"\bproc\.?\b", "processo"),
    (r"\bfisc\.?\b", "fiscal"),
    (r"\bdef\.?\b", "defesa"),
    (r"\bsust\.?\b", "sustentacao"),
    (r"\bprep\.?\b", "preparacao"),
    (r"\bcorresp\.?\b", "correspondencia"),
]


def normalizar_texto(s: object) -> str:
    """lowercase, sem acentos, espaços colapsados, abreviações expandidas.

    Idempotente. Retorna string vazia para None / NaN.
    """
    if s is None:
        return ""
    if isinstance(s, float) and pd.isna(s):
        return ""
    t = unidecode(str(s)).lower()
    # remove pontuação leve mas preserva separadores úteis
    t = re.sub(r"[\"\'`]", "", t)
    t = re.sub(r"\s+", " ", t).strip()
    for padrao, sub in ABREVIACOES:
        t = re.sub(padrao, sub, t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def aplicar(df: pd.DataFrame, mapa_colunas: dict[str, str], colunas_texto: list[str]) -> pd.DataFrame:
    """Adiciona colunas '<canonico>_norm' com texto normalizado.

    Não altera as colunas originais. Cria também coluna `_id_origem` se não existir.
    """
    out = df.copy()
    if "_id_origem" not in out.columns:
        out.insert(0, "_id_origem", range(1, len(out) + 1))
    for canonico in colunas_texto:
        col_real = mapa_colunas.get(canonico)
        if col_real is None:
            out[f"{canonico}_norm"] = ""
        else:
            out[f"{canonico}_norm"] = out[col_real].map(normalizar_texto)
    return out
