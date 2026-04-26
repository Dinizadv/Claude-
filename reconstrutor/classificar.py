"""Detecção do núcleo da atividade na descrição.

Cada núcleo tem chave canônica + padrões pt/en + verbo padrão por idioma.
Múltiplos núcleos detectados sinalizam possível desdobramento.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Nucleo:
    chave: str
    verbo_pt: str
    verbo_en: str
    objeto_pt: str
    objeto_en: str


# Ordem importa só para reprodutibilidade quando o score empata.
NUCLEOS: list[Nucleo] = [
    Nucleo("analise_documentos", "Análise", "Analysis", "de documentos", "of documents"),
    Nucleo("pesquisa", "Pesquisa", "Research", "jurídica", "on legal aspects"),
    Nucleo("reuniao_interna", "Reunião interna", "Internal meeting", "para alinhamento", "for alignment"),
    Nucleo("conference_call", "Conference call", "Conference call", "com o cliente", "with the client"),
    Nucleo("parecer_elaboracao", "Elaboração", "Drafting", "de parecer", "of legal opinion"),
    Nucleo("parecer_revisao", "Revisão", "Review", "de parecer", "of legal opinion"),
    Nucleo("peticao_elaboracao", "Elaboração", "Drafting", "de petição", "of pleading"),
    Nucleo("peticao_revisao", "Revisão", "Review", "de petição", "of pleading"),
    Nucleo("decisao_administrativa", "Análise", "Analysis", "de decisão administrativa", "of administrative decision"),
    Nucleo("decisao_judicial", "Análise", "Analysis", "de decisão judicial", "of judicial decision"),
    Nucleo("diligencia", "Diligência", "Diligence", "processual", "in proceedings"),
    Nucleo("correspondencia", "Correspondência", "Correspondence", "consultiva", "drafting"),
    Nucleo("entendimento_interno", "Discussão interna", "Internal discussion", "sobre o caso", "on the matter"),
    Nucleo("julgamento", "Acompanhamento", "Monitoring", "de sessão de julgamento", "of judgment session"),
    Nucleo("due_diligence", "Due diligence", "Due diligence", "documental", "on documents"),
    Nucleo("contrato", "Análise", "Analysis", "contratual", "of contractual matters"),
]


# Padrões de palavras que disparam cada núcleo. Texto já normalizado (sem acentos, lower).
PADROES: dict[str, list[str]] = {
    "analise_documentos":   ["analise de documento", "analise documental", "analise docs", "analise doc", "review of document", "document analysis", "analysis of documents", "analysis of document"],
    "pesquisa":             ["pesquisa", "research", "consolidacao de entendimento", "levantamento"],
    "reuniao_interna":      ["reuniao interna", "reuniao", "internal meeting", "alinhamento interno", "discussao interna"],
    "conference_call":      ["conference call", "call com", "call ", "ligacao com", "video call"],
    "parecer_elaboracao":   ["elaboracao de parecer", "minuta de parecer", "drafting opinion", "parecer "],
    "parecer_revisao":      ["revisao de parecer", "review of legal opinion", "review opinion", "revisao do parecer"],
    "peticao_elaboracao":   ["elaboracao de peticao", "minuta de peticao", "drafting pleading", "peticao "],
    "peticao_revisao":      ["revisao de peticao", "revisao da peticao", "review pleading"],
    "decisao_administrativa": ["decisao administrativa", "auto de infracao", "carf", "delegacia da receita", "administrative decision"],
    "decisao_judicial":     ["decisao judicial", "sentenca", "acordao", "judicial decision"],
    "diligencia":           ["diligencia", "andamento processual", "filing", "protocolo"],
    "correspondencia":      ["correspondencia", "email para", "email com", "correspondence"],
    "entendimento_interno": ["entendimento interno", "alinhamento sobre", "estrategia", "definicao de estrategia"],
    "julgamento":           ["sessao de julgamento", "julgamento", "judgment session", "tribunal", "sustentacao oral", "preparacao para sustentacao", "sustentacao"],
    "due_diligence":        ["due diligence", "auditoria documental"],
    "contrato":             ["contrato", "minuta contratual", "contractual"],
}


def detectar(descricao_norm: str) -> list[Nucleo]:
    """Retorna lista de núcleos detectados, ordenados por especificidade.

    Match é por substring na descrição normalizada. Sem hits → lista vazia.
    """
    if not descricao_norm:
        return []
    encontrados: list[Nucleo] = []
    for nucleo in NUCLEOS:
        for padrao in PADROES.get(nucleo.chave, []):
            if padrao in descricao_norm:
                encontrados.append(nucleo)
                break
    return encontrados


def nucleo_principal(nucleos: list[Nucleo]) -> Nucleo | None:
    return nucleos[0] if nucleos else None
