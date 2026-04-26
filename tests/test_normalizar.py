"""Testes de normalização textual."""

from __future__ import annotations

from reconstrutor.normalizar import normalizar_texto


def test_lower_e_unidecode():
    assert normalizar_texto("Análise") == "analise"
    assert normalizar_texto("DECISÃO JUDICIAL") == "decisao judicial"


def test_colapsa_espacos():
    assert normalizar_texto("a   b\tc\n d") == "a b c d"


def test_none_e_vazio():
    assert normalizar_texto(None) == ""
    assert normalizar_texto("") == ""


def test_expande_abreviacoes():
    assert "classificacao fiscal" in normalizar_texto("PARECER CLASSI.FISC.")
    assert "analise" in normalizar_texto("ANAL. de docs")
    assert "documentos" in normalizar_texto("ANAL. de docs")


def test_idempotente():
    s = "Análise de docs sobre classi.fisc."
    n1 = normalizar_texto(s)
    n2 = normalizar_texto(n1)
    assert n1 == n2
