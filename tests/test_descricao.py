"""Testes da reescrita de descrição."""

from __future__ import annotations

from reconstrutor.classificar import detectar, nucleo_principal
from reconstrutor.descricao import reescrever


def test_reescrita_pt_com_tema():
    nucleos = detectar("analise de documentos sobre classificacao fiscal")
    n = nucleo_principal(nucleos)
    final, foi = reescrever(n, "Análise de docs", "analise de documentos sobre classificacao fiscal", "POSITIVO", "pt")
    assert foi
    assert "Análise" in final
    assert "POSITIVO" in final
    assert "classificação fiscal" in final


def test_reescrita_en():
    nucleos = detectar("analysis of documents regarding indirect tax")
    n = nucleo_principal(nucleos)
    final, foi = reescrever(n, "orig", "analysis of documents regarding indirect tax", "INPEK", "en")
    assert foi
    assert "Analysis" in final or "analysis" in final.lower()
    assert "INPEK" in final


def test_sem_nucleo_preserva_original():
    final, foi = reescrever(None, "ajustes", "ajustes", None, "pt")
    assert not foi
    assert final == "ajustes"


def test_termina_com_ponto():
    nucleos = detectar("reuniao interna sobre creditamento fiscal")
    n = nucleo_principal(nucleos)
    final, _ = reescrever(n, "orig", "reuniao interna sobre creditamento fiscal", "POSITIVO", "pt")
    assert final.endswith(".")
