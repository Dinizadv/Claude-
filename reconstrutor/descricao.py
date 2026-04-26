"""Reescrita da descrição final no padrão da equipe."""

from __future__ import annotations

from .classificar import Nucleo
from .esquema import IDIOMA_EN, IDIOMA_PT


def _complemento_tema(descricao_norm: str, idioma: str) -> str:
    """Tenta extrair um complemento temático curto da descrição original.

    Procura por palavras-chave de matéria; se nada encontrar, retorna string vazia.
    """
    temas_pt = {
        "classificacao fiscal": "classificação fiscal",
        "aduaneiro":            "matéria aduaneira",
        "itbi":                 "incidência de ITBI",
        "icms":                 "incidência de ICMS",
        "iss":                  "incidência de ISS",
        "irpj":                 "incidência de IRPJ",
        "creditamento":         "creditamento fiscal",
        "devolucao":            "devolução de mercadorias",
        "transferencia":        "transferência de bens",
        "auto de infracao":     "auto de infração",
        "execucao fiscal":      "execução fiscal",
        "societario":           "matéria societária",
        "consultivo":           "tema consultivo",
    }
    temas_en = {
        "classificacao fiscal": "tax classification of products",
        "aduaneiro":            "customs matters",
        "itbi":                 "real estate transfer tax",
        "icms":                 "indirect tax",
        "iss":                  "service tax",
        "irpj":                 "corporate income tax",
        "creditamento":         "tax crediting",
        "devolucao":            "return of goods",
        "transferencia":        "symbolic transfer of goods",
        "auto de infracao":     "tax assessment",
        "execucao fiscal":      "tax foreclosure",
        "societario":           "corporate matters",
    }
    tabela = temas_en if idioma == IDIOMA_EN else temas_pt
    for chave, valor in tabela.items():
        if chave in descricao_norm:
            return valor
    return ""


def reescrever(
    nucleo: Nucleo | None,
    descricao_original: str,
    descricao_norm: str,
    cliente: str | None,
    idioma: str,
) -> tuple[str, bool]:
    """Retorna (descricao_final, foi_reescrita).

    Se não houver núcleo identificável, devolve a descrição original limpa
    com flag False para sinalizar que a reescrita não foi possível.
    """
    if nucleo is None:
        return descricao_original.strip(), False

    tema = _complemento_tema(descricao_norm, idioma)

    if idioma == IDIOMA_EN:
        partes = [f"{nucleo.verbo_en} {nucleo.objeto_en}"]
        if tema:
            partes.append(f"regarding {tema}")
        if cliente:
            partes.append(f"({cliente})")
        return " ".join(partes).strip().rstrip(".") + ".", True

    partes = [f"{nucleo.verbo_pt} {nucleo.objeto_pt}"]
    if tema:
        partes.append(f"relacionada à {tema}" if tema.startswith(("matéria", "incidência")) else f"sobre {tema}")
    if cliente:
        partes.append(f"({cliente})")
    return " ".join(partes).strip().rstrip(".") + ".", True
