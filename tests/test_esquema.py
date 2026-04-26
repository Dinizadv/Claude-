"""Testes do mapeador de colunas canônicas."""

from __future__ import annotations

import pytest

from reconstrutor import esquema


def test_mapear_colunas_basico():
    cols = ["Descrição", "Data início", "Tempo total", "Executante"]
    mapa = esquema.mapear_colunas(cols, esquema.ALIASES_USUARIO)
    assert mapa["descricao"] == "Descrição"
    assert mapa["data_inicio"] == "Data início"
    assert mapa["duracao"] == "Tempo total"
    assert mapa["executante"] == "Executante"


def test_aliases_case_insensitive_e_acentos():
    cols = ["DESCRICAO", "DATA_DE_INICIO", "DURAÇÃO"]
    mapa = esquema.mapear_colunas(cols, esquema.ALIASES_USUARIO)
    assert mapa["descricao"] == "DESCRICAO"
    assert mapa["data_inicio"] == "DATA_DE_INICIO"
    assert mapa["duracao"] == "DURAÇÃO"


def test_colunas_faltantes():
    mapa = {"descricao": "X"}
    falt = esquema.colunas_faltantes(mapa, esquema.OBRIGATORIAS_USUARIO)
    assert "data_inicio" in falt
    assert "duracao" in falt


def test_obrigatorias_equipe():
    cols = ["Descricao", "Data", "Tempo", "Cliente", "Pasta", "Vinculo"]
    mapa = esquema.mapear_colunas(cols, esquema.ALIASES_EQUIPE)
    assert esquema.colunas_faltantes(mapa, esquema.OBRIGATORIAS_EQUIPE) == []
