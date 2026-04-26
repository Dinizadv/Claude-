"""Identificação do cliente provável a partir da descrição.

Estratégia:
1. Constrói índice cliente -> {tokens, freq, descricoes_normalizadas} a partir da equipe.
2. Para cada linha do usuário, tenta:
   a. match exato de nome/sigla normalizada na descrição;
   b. fuzzy match contra blob de descrições por cliente (rapidfuzz);
   c. score combinado.
3. Exige no mínimo 2 indícios para alta confiança.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

import pandas as pd
from rapidfuzz import fuzz

from .normalizar import normalizar_texto


@dataclass
class CandidatoCliente:
    nome: str            # nome real do cliente como aparece na base
    score: float         # 0..1
    indicios: list[str]  # razões textuais


def _siglas_e_tokens(nome: str) -> set[str]:
    """Gera variações pesquisáveis a partir do nome do cliente."""
    n = normalizar_texto(nome)
    tokens = set(re.findall(r"[a-z0-9]+", n))
    # tokens muito curtos viram ruído; mantém apenas com 3+ chars
    tokens = {t for t in tokens if len(t) >= 3}
    # adiciona o nome inteiro normalizado
    tokens.add(n)
    return tokens


def construir_indice(df_equipe: pd.DataFrame, mapa: dict[str, str]) -> dict[str, dict]:
    """Retorna {cliente_real: {tokens, freq, blob_norm, descricoes_norm}}."""
    col_cliente = mapa["cliente"]
    indice: dict[str, dict] = {}
    for _, row in df_equipe.iterrows():
        nome = row.get(col_cliente)
        if nome is None or (isinstance(nome, float) and pd.isna(nome)):
            continue
        nome = str(nome).strip()
        if not nome:
            continue
        entry = indice.setdefault(
            nome,
            {"tokens": _siglas_e_tokens(nome), "freq": 0, "descricoes_norm": []},
        )
        entry["freq"] += 1
        desc = row.get("descricao_norm", "") or normalizar_texto(row.get(mapa.get("descricao", ""), ""))
        if desc:
            entry["descricoes_norm"].append(desc)
    for nome, entry in indice.items():
        entry["blob_norm"] = " | ".join(entry["descricoes_norm"])
    return indice


def identificar(descricao_norm: str, indice: dict[str, dict]) -> CandidatoCliente | None:
    """Retorna o melhor candidato ou None se nada bater minimamente."""
    if not descricao_norm or not indice:
        return None

    melhores: list[CandidatoCliente] = []
    for nome, entry in indice.items():
        indicios: list[str] = []
        score = 0.0

        # (a) match direto por sigla/token
        tokens_hit = [t for t in entry["tokens"] if t and t in descricao_norm]
        if tokens_hit:
            # token mais longo casado pesa mais
            mais_longo = max(len(t) for t in tokens_hit)
            score += min(0.6, 0.15 + 0.05 * mais_longo)
            indicios.append(f"token:{','.join(sorted(tokens_hit)[:3])}")

        # (b) fuzzy contra blob (cap em 0.4 para não dominar)
        if entry["blob_norm"]:
            f = fuzz.partial_ratio(descricao_norm, entry["blob_norm"]) / 100.0
            if f >= 0.6:
                score += min(0.4, (f - 0.5) * 0.6)
                indicios.append(f"fuzzy:{f:.2f}")

        # (c) bonus por frequência relativa (até +0.1)
        score += min(0.1, entry["freq"] / 100.0)

        if score > 0:
            melhores.append(CandidatoCliente(nome=nome, score=min(1.0, score), indicios=indicios))

    if not melhores:
        return None
    melhores.sort(key=lambda c: c.score, reverse=True)
    top = melhores[0]
    # threshold mínimo: sem hit direto de token e fuzzy fraco => não atribui cliente
    tem_token_hit = any(i.startswith("token:") for i in top.indicios)
    if not tem_token_hit and top.score < 0.3:
        return None
    # se 1º e 2º muito próximos, reduz confiança e registra
    if len(melhores) > 1 and (top.score - melhores[1].score) < 0.05:
        top = CandidatoCliente(
            nome=top.nome,
            score=top.score * 0.85,
            indicios=top.indicios + [f"empate_com:{melhores[1].nome}"],
        )
    return top
