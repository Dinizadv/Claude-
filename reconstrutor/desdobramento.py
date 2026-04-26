"""Detecção de possível desdobramento (múltiplas atividades numa só linha)."""

from __future__ import annotations

import re

from .classificar import Nucleo


# Conectores que costumam unir atividades distintas em uma mesma anotação.
CONECTORES = [r"\s\+\s", r"\be\b", r"\bcom\b\s+\w+\s+e\b", r"\bmais\b"]


def detectar(descricao_norm: str, nucleos: list[Nucleo]) -> bool:
    """Retorna True se há indício de mais de uma atividade.

    Critérios (Etapa 10 da spec):
      - 2 ou mais núcleos distintos detectados;
      - presença de conectores típicos de aditivo somada a um núcleo qualquer.
    """
    if len(nucleos) >= 2:
        return True
    if not nucleos:
        return False
    for padrao in CONECTORES:
        if re.search(padrao, descricao_norm):
            # com 1 núcleo + conector, considera apenas se houver 2+ verbos
            verbos = ["analise", "pesquisa", "revisao", "elaboracao", "reuniao", "call", "discussao"]
            hits = sum(1 for v in verbos if v in descricao_norm)
            if hits >= 2:
                return True
    return False
