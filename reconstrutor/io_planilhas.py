"""Leitura de planilhas .xlsx com detecção flexível de colunas."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from . import esquema


@dataclass
class Planilha:
    """Conjunto canonizado de DataFrame + mapa de colunas."""

    df: pd.DataFrame
    mapa: dict[str, str]
    caminho: Path

    def col(self, canonico: str) -> str | None:
        return self.mapa.get(canonico)


def ler(caminho: str | Path, aliases: dict[str, list[str]], obrigatorias: list[str]) -> Planilha:
    """Lê um .xlsx, detecta colunas pelo mapa de aliases e valida obrigatórias.

    Lança ValueError com mensagem clara se faltar coluna obrigatória.
    """
    caminho = Path(caminho)
    if not caminho.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")

    df = pd.read_excel(caminho, dtype=object)
    df.columns = [str(c).strip() for c in df.columns]
    mapa = esquema.mapear_colunas(list(df.columns), aliases)
    faltantes = esquema.colunas_faltantes(mapa, obrigatorias)
    if faltantes:
        raise ValueError(
            f"Arquivo {caminho.name}: colunas obrigatórias não encontradas: {faltantes}. "
            f"Cabeçalhos presentes: {list(df.columns)}"
        )
    return Planilha(df=df, mapa=mapa, caminho=caminho)
