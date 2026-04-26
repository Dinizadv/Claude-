"""Teste end-to-end do pipeline contra as fixtures sintéticas."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from reconstrutor.pipeline import reconstruir


@pytest.fixture
def saida(tmp_path: Path, caminho_fixture_a, caminho_fixture_b):
    out = tmp_path / "saida.xlsx"
    resumo = reconstruir(caminho_fixture_a, caminho_fixture_b, out)
    return out, resumo


def test_resumo_basico(saida):
    out, resumo = saida
    assert out.exists()
    assert resumo.total == 10
    assert resumo.alta + resumo.media + resumo.baixa == 10
    assert resumo.baixa >= 2  # casos 4 (ajustes) e 8 (jurisprudência geral) ao menos


def test_seis_abas(saida):
    out, _ = saida
    xls = pd.ExcelFile(out)
    esperadas = {"README", "RAW_USUARIO", "RAW_EQUIPE", "SUGESTOES_FINAIS",
                 "CASOS_DUVIDOSOS", "PASTAS_REFERENCIADAS"}
    assert esperadas.issubset(set(xls.sheet_names))


def test_sugestoes_tem_20_colunas(saida):
    out, _ = saida
    df = pd.read_excel(out, sheet_name="SUGESTOES_FINAIS")
    assert df.shape == (10, 20)


def test_data_inicio_e_duracao_preservadas(saida, caminho_fixture_a):
    """Regra crítica: data de início e duração não são alteradas."""
    out, _ = saida
    df_orig = pd.read_excel(caminho_fixture_a)
    df_sug = pd.read_excel(out, sheet_name="SUGESTOES_FINAIS")
    # mesma ordem (ID origem 1..10)
    for i in range(10):
        orig_data = pd.Timestamp(df_orig.iloc[i]["Data inicio"]).date().isoformat()
        sug_data = str(df_sug.iloc[i]["Data de início"])
        assert orig_data in sug_data, f"linha {i+1}: data não preservada"
    # duração original copiada
    assert (df_sug["Duração original"] == df_sug["Tempo total resultante"]).all()


def test_hora_inicio_sugerida_zero(saida):
    out, _ = saida
    df = pd.read_excel(out, sheet_name="SUGESTOES_FINAIS")
    assert (df["Hora de início sugerida"].astype(str) == "00:00").all()


def test_pastas_nunca_inventadas(saida):
    """Linhas sem cliente claro não devem ter pasta atribuída."""
    out, _ = saida
    df = pd.read_excel(out, sheet_name="SUGESTOES_FINAIS")
    for _, r in df.iterrows():
        if not str(r["Cliente sugerido"]).strip() or pd.isna(r["Cliente sugerido"]):
            assert pd.isna(r["Número da pasta sugerida"]) or str(r["Número da pasta sugerida"]).strip() == ""


def test_descricao_em_ingles_para_inpek(saida):
    out, _ = saida
    df = pd.read_excel(out, sheet_name="SUGESTOES_FINAIS")
    inpek = df[df["Cliente sugerido"] == "INPEK"]
    assert not inpek.empty
    assert (inpek["Idioma sugerido"] == "en").all()


def test_desdobramento_marca_caso_com_mais_e_call(saida):
    """Linha 6 do fixture tem '+' e dois núcleos (análise e call)."""
    out, _ = saida
    df = pd.read_excel(out, sheet_name="SUGESTOES_FINAIS")
    linha6 = df[df["ID origem"] == 6].iloc[0]
    assert bool(linha6["Indício de desdobramento?"]) is True


def test_casos_duvidosos_subset(saida):
    out, _ = saida
    df_sug = pd.read_excel(out, sheet_name="SUGESTOES_FINAIS")
    df_dub = pd.read_excel(out, sheet_name="CASOS_DUVIDOSOS")
    # CASOS_DUVIDOSOS é subset de SUGESTOES_FINAIS por ID origem
    assert set(df_dub["ID origem"]).issubset(set(df_sug["ID origem"]))
    # toda linha baixa aparece em duvidosos
    baixas = set(df_sug[df_sug["Grau de confiança"] == "baixa"]["ID origem"])
    assert baixas.issubset(set(df_dub["ID origem"]))


def test_pastas_referenciadas_existem_no_arquivo_b(saida, caminho_fixture_b):
    out, _ = saida
    df_b = pd.read_excel(caminho_fixture_b)
    df_pas = pd.read_excel(out, sheet_name="PASTAS_REFERENCIADAS")
    assert set(df_pas["Número da pasta"].astype(str)).issubset(set(df_b["Pasta"].astype(str)))
