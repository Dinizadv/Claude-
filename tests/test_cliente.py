"""Testes da identificação de cliente."""

from __future__ import annotations

import pandas as pd
import pytest

from reconstrutor.cliente import construir_indice, identificar
from reconstrutor.normalizar import normalizar_texto


@pytest.fixture
def indice():
    df = pd.DataFrame([
        {"Cliente": "POSITIVO", "Descricao": "analise de documentos sobre materia aduaneira"},
        {"Cliente": "POSITIVO", "Descricao": "pesquisa sobre creditamento fiscal"},
        {"Cliente": "INPEK", "Descricao": "analysis of documents regarding indirect tax"},
        {"Cliente": "SCHAR", "Descricao": "peticao de impugnacao a auto de infracao"},
    ])
    df["descricao_norm"] = df["Descricao"].map(normalizar_texto)
    mapa = {"cliente": "Cliente", "descricao": "Descricao"}
    return construir_indice(df, mapa)


def test_match_token_direto(indice):
    c = identificar("positivo - analise de documentos", indice)
    assert c is not None
    assert c.nome == "POSITIVO"


def test_sem_match_retorna_none(indice):
    """Descrição sem cliente identificável não deve atribuir cliente espúrio."""
    assert identificar("ajustes", indice) is None
    assert identificar("leitura de jurisprudencia geral", indice) is None


def test_descricao_vazia_retorna_none(indice):
    assert identificar("", indice) is None


def test_match_inpek(indice):
    c = identificar("inpek - call com cliente sobre indirect tax", indice)
    assert c is not None
    assert c.nome == "INPEK"
