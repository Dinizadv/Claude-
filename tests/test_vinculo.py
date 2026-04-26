"""Testes da decisão SERV vs PROC."""

from __future__ import annotations

import pandas as pd
import pytest

from reconstrutor.esquema import VINCULO_DUVIDA, VINCULO_PROC, VINCULO_SERV
from reconstrutor.vinculo import decidir


@pytest.fixture
def df_vazio():
    return pd.DataFrame(columns=["Cliente", "Vinculo"]), {"cliente": "Cliente", "vinculo": "Vinculo"}


def test_palavra_serv_forte_vence_historico_proc():
    """SCHAR é predominantemente PROC, mas 'parecer' deve dominar e ir para SERV."""
    df = pd.DataFrame([
        {"Cliente": "SCHAR", "Vinculo": "PROC"},
        {"Cliente": "SCHAR", "Vinculo": "PROC"},
        {"Cliente": "SCHAR", "Vinculo": "SERV"},
    ])
    mapa = {"cliente": "Cliente", "vinculo": "Vinculo"}
    d = decidir("schar parecer classificacao fiscal revisao", "SCHAR", df, mapa)
    assert d.vinculo == VINCULO_SERV


def test_numero_cnj_forca_proc(df_vazio):
    df, mapa = df_vazio
    d = decidir("analise sobre 1234567-89.2024.1.23.4567", None, df, mapa)
    assert d.vinculo == VINCULO_PROC


def test_auto_de_infracao_forca_proc(df_vazio):
    df, mapa = df_vazio
    d = decidir("peticao de impugnacao a auto de infracao", None, df, mapa)
    assert d.vinculo == VINCULO_PROC


def test_parecer_isolado_eh_serv(df_vazio):
    df, mapa = df_vazio
    d = decidir("revisao de parecer sobre tema consultivo", None, df, mapa)
    assert d.vinculo == VINCULO_SERV


def test_sem_sinais_retorna_duvida(df_vazio):
    df, mapa = df_vazio
    d = decidir("ajustes", None, df, mapa)
    assert d.vinculo == VINCULO_DUVIDA


def test_historico_serve_de_tiebreaker():
    """Sem palavras-chave fortes, histórico decide."""
    df = pd.DataFrame([
        {"Cliente": "X", "Vinculo": "SERV"},
        {"Cliente": "X", "Vinculo": "SERV"},
        {"Cliente": "X", "Vinculo": "SERV"},
    ])
    mapa = {"cliente": "Cliente", "vinculo": "Vinculo"}
    # 'pesquisa' é SERV peso 1; histórico SERV +1 → score_serv=2, score_proc=0
    d = decidir("pesquisa juridica", "X", df, mapa)
    assert d.vinculo == VINCULO_SERV
