"""Aliases canônicos para colunas dos arquivos de entrada."""

from __future__ import annotations

from unidecode import unidecode


VINCULO_SERV = "SERV"
VINCULO_PROC = "PROC"
VINCULO_DUVIDA = "DUVIDA"

CONF_ALTA = "alta"
CONF_MEDIA = "media"
CONF_BAIXA = "baixa"

IDIOMA_PT = "pt"
IDIOMA_EN = "en"


# Aliases por nome canônico. Cada alias é comparado contra o cabeçalho normalizado
# (lower + unidecode + collapse spaces). A primeira coluna que casar é adotada.
ALIASES_USUARIO: dict[str, list[str]] = {
    "descricao":   ["descricao", "descrição", "atividade", "historico", "histórico", "obs", "observacao", "observação"],
    "data_inicio": ["data inicio", "data início", "data de inicio", "data de início", "data inicial", "inicio", "início", "data"],
    "hora_inicio": ["hora inicio", "hora início", "hora inicial", "horario inicio", "horário início"],
    "data_fim":    ["data fim", "data final", "data de fim", "data de término", "data termino"],
    "hora_fim":    ["hora fim", "hora final", "hora termino", "hora término"],
    "duracao":     ["duracao", "duração", "tempo", "tempo total", "horas", "tempo gasto"],
    "executante":  ["executante", "responsavel", "responsável", "advogado", "usuario", "usuário"],
    "pasta_orig":  ["pasta", "pasta original", "matter"],
}

ALIASES_EQUIPE: dict[str, list[str]] = {
    "descricao":     ["descricao", "descrição", "atividade", "historico", "histórico"],
    "data_inicio":   ["data inicio", "data início", "data de inicio", "data de início", "data inicial", "inicio", "início", "data"],
    "duracao":       ["duracao", "duração", "tempo", "tempo total", "horas"],
    "executante":    ["executante", "responsavel", "responsável", "advogado"],
    "cliente":       ["cliente", "client", "customer"],
    "numero_pasta":  ["numero pasta", "número pasta", "no pasta", "n pasta", "pasta", "matter", "matter no", "numero"],
    "nome_pasta":    ["nome pasta", "nome da pasta", "matter name", "descricao pasta", "descrição pasta"],
    "vinculo":       ["vinculo", "vínculo", "tipo vinculo", "tipo vínculo", "serv/proc", "serv proc", "scope", "tipo"],
    "tipo_subtipo":  ["tipo subtipo", "tipo/subtipo", "type/subtype", "type subtype", "classificacao", "classificação"],
    "idioma":        ["idioma", "language", "lang"],
}


def _canonizar_cabecalho(s: str) -> str:
    """Normaliza um cabeçalho para comparação com aliases."""
    if s is None:
        return ""
    t = unidecode(str(s)).lower().strip()
    # colapsa espaços e troca underscores/hífens por espaço
    t = t.replace("_", " ").replace("-", " ")
    while "  " in t:
        t = t.replace("  ", " ")
    return t


def mapear_colunas(colunas: list[str], aliases: dict[str, list[str]]) -> dict[str, str]:
    """Retorna mapa nome_canonico -> nome_real_no_arquivo.

    Para cada nome canônico, escolhe a primeira coluna real cujo cabeçalho
    canonizado bata com qualquer um dos aliases. Aliases também são canonizados.
    """
    cabecalhos = {col: _canonizar_cabecalho(col) for col in colunas}
    mapa: dict[str, str] = {}
    for canonico, lista_alias in aliases.items():
        alvos = {_canonizar_cabecalho(a) for a in lista_alias}
        for col_real, col_norm in cabecalhos.items():
            if col_norm in alvos and col_real not in mapa.values():
                mapa[canonico] = col_real
                break
    return mapa


def colunas_faltantes(mapa: dict[str, str], obrigatorias: list[str]) -> list[str]:
    return [c for c in obrigatorias if c not in mapa]


OBRIGATORIAS_USUARIO = ["descricao", "data_inicio", "duracao"]
OBRIGATORIAS_EQUIPE = ["descricao", "cliente", "numero_pasta", "vinculo"]
