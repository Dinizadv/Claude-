"""Sugere tipo/subtipo a partir do histórico da pasta escolhida."""

from __future__ import annotations

from .pasta import CandidatoPasta
from .classificar import Nucleo


# Mapeamento conservador núcleo -> tipo/subtipo padrão (pt e en).
# Usado só como fallback quando a pasta não tem histórico de tipo/subtipo.
PADRAO_PT: dict[str, str] = {
    "analise_documentos":      "Análise de documentos",
    "pesquisa":                "Pesquisa",
    "reuniao_interna":         "Reunião | interna",
    "conference_call":         "Conference Call",
    "parecer_elaboracao":      "Parecer | elaboração",
    "parecer_revisao":         "Parecer | revisão, alterações e redação final",
    "peticao_elaboracao":      "Petição | elaboração",
    "peticao_revisao":         "Petição | revisão, alterações e redação final",
    "decisao_administrativa":  "Análise de decisão administrativa",
    "decisao_judicial":        "Análise de decisão judicial",
    "diligencia":              "Diligência",
    "correspondencia":         "Correspondência",
    "entendimento_interno":    "Reunião | interna",
    "julgamento":              "Acompanhamento de julgamento",
    "due_diligence":           "Análise de documentos",
    "contrato":                "Análise de documentos",
}

PADRAO_EN: dict[str, str] = {
    "analise_documentos":      "Document | analysis",
    "pesquisa":                "Research",
    "reuniao_interna":         "Internal meeting",
    "conference_call":         "Conference Call",
    "parecer_elaboracao":      "Legal Opinion | drafting",
    "parecer_revisao":         "Legal Opinion | review, changes and final wording",
    "peticao_elaboracao":      "Pleading | drafting",
    "peticao_revisao":         "Pleading | review, changes and final wording",
    "decisao_administrativa":  "Administrative decision | analysis",
    "decisao_judicial":        "Judicial decision | analysis",
    "diligencia":              "Filing",
    "correspondencia":         "Correspondence | drafting",
    "entendimento_interno":    "Internal meeting",
    "julgamento":              "Judgment session | monitoring",
    "due_diligence":           "Document | analysis",
    "contrato":                "Document | analysis",
}


def escolher(pasta: CandidatoPasta | None, nucleo: Nucleo | None, idioma: str) -> str:
    """Retorna o tipo/subtipo mais aderente.

    Hierarquia:
      1. Tipo mais frequente da pasta no histórico da equipe.
      2. Padrão do núcleo no idioma sugerido.
      3. String vazia se nada disponível.
    """
    if pasta and pasta.tipos_subtipos:
        return pasta.tipos_subtipos[0]
    if nucleo:
        tabela = PADRAO_EN if idioma == "en" else PADRAO_PT
        return tabela.get(nucleo.chave, "")
    return ""
