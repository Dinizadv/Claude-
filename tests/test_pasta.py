"""Testes do lookup de pastas."""

from __future__ import annotations

import pandas as pd
import pytest

from reconstrutor.esquema import IDIOMA_EN, IDIOMA_PT
from reconstrutor.pasta import construir_indice, escolher


@pytest.fixture
def base_equipe():
    df = pd.DataFrame([
        {"Cliente": "POSITIVO", "Pasta": "10001", "Nome": "POSITIVO - ADUANEIRO",
         "Vinculo": "SERV", "Tipo": "Análise de documentos",
         "Descricao": "Análise de documentos sobre matéria aduaneira."},
        {"Cliente": "POSITIVO", "Pasta": "10001", "Nome": "POSITIVO - ADUANEIRO",
         "Vinculo": "SERV", "Tipo": "Análise de documentos",
         "Descricao": "Análise de documentos sobre matéria aduaneira."},
        {"Cliente": "POSITIVO", "Pasta": "10002", "Nome": "POSITIVO - CONSULTIVO",
         "Vinculo": "SERV", "Tipo": "Reunião | interna",
         "Descricao": "Reunião interna para alinhamento."},
        {"Cliente": "INPEK", "Pasta": "30001", "Nome": "INPEK - INTERNATIONAL TAX",
         "Vinculo": "SERV", "Tipo": "Document | analysis",
         "Descricao": "Analysis of documents regarding indirect tax."},
    ])
    mapa = {
        "cliente": "Cliente", "numero_pasta": "Pasta", "nome_pasta": "Nome",
        "vinculo": "Vinculo", "tipo_subtipo": "Tipo", "descricao": "Descricao",
    }
    return df, mapa


def test_indice_agrega_por_cliente_vinculo_pasta(base_equipe):
    df, mapa = base_equipe
    idx = construir_indice(df, mapa)
    chaves = {(c.cliente, c.vinculo, c.numero) for c in idx}
    assert ("POSITIVO", "SERV", "10001") in chaves
    assert ("POSITIVO", "SERV", "10002") in chaves
    assert ("INPEK", "SERV", "30001") in chaves


def test_idioma_en_detectado(base_equipe):
    df, mapa = base_equipe
    idx = construir_indice(df, mapa)
    inpek = next(c for c in idx if c.cliente == "INPEK")
    assert inpek.idioma == IDIOMA_EN


def test_idioma_pt_detectado(base_equipe):
    df, mapa = base_equipe
    idx = construir_indice(df, mapa)
    pos = next(c for c in idx if c.cliente == "POSITIVO" and c.numero == "10001")
    assert pos.idioma == IDIOMA_PT


def test_escolher_nunca_inventa(base_equipe):
    df, mapa = base_equipe
    idx = construir_indice(df, mapa)
    principal, alt = escolher("CLIENTE_INEXISTENTE", "SERV", "qualquer descricao", idx)
    assert principal is None
    assert alt is None


def test_escolher_pasta_mais_frequente(base_equipe):
    df, mapa = base_equipe
    idx = construir_indice(df, mapa)
    principal, _ = escolher("POSITIVO", "SERV", "analise documentos aduaneiro", idx)
    assert principal is not None
    assert principal.numero == "10001"


def test_escolher_registra_alternativa(base_equipe):
    """Quando há 2 pastas com freq comparável, alternativa deve ser preenchida."""
    df = pd.DataFrame([
        {"Cliente": "X", "Pasta": "1", "Nome": "X-A", "Vinculo": "SERV", "Tipo": "T1", "Descricao": "abc"},
        {"Cliente": "X", "Pasta": "1", "Nome": "X-A", "Vinculo": "SERV", "Tipo": "T1", "Descricao": "abc"},
        {"Cliente": "X", "Pasta": "2", "Nome": "X-B", "Vinculo": "SERV", "Tipo": "T1", "Descricao": "abc"},
        {"Cliente": "X", "Pasta": "2", "Nome": "X-B", "Vinculo": "SERV", "Tipo": "T1", "Descricao": "abc"},
    ])
    mapa = {"cliente": "Cliente", "numero_pasta": "Pasta", "nome_pasta": "Nome",
            "vinculo": "Vinculo", "tipo_subtipo": "Tipo", "descricao": "Descricao"}
    idx = construir_indice(df, mapa)
    principal, alt = escolher("X", "SERV", "qualquer", idx)
    assert principal is not None
    assert alt is not None
    assert principal.numero != alt.numero
