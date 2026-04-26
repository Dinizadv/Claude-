"""Orquestração do pipeline de reconstrução."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd

from . import (
    cliente as mod_cliente,
    classificar,
    confianca,
    desdobramento,
    descricao,
    esquema,
    idioma as mod_idioma,
    io_planilhas,
    normalizar,
    pasta as mod_pasta,
    saida,
    tipo_subtipo,
    vinculo as mod_vinculo,
)


@dataclass
class Resumo:
    total: int
    alta: int
    media: int
    baixa: int
    revisao_humana: int
    desdobramento: int


def _hora_inicio_sugerida() -> str:
    return "00:00"


def _formatar_data(v: Any) -> Any:
    if v is None:
        return None
    if isinstance(v, float) and pd.isna(v):
        return None
    if isinstance(v, pd.Timestamp):
        return v.date().isoformat()
    return v


def reconstruir(path_a: str | Path, path_b: str | Path, path_out: str | Path) -> Resumo:
    path_a = Path(path_a)
    path_b = Path(path_b)
    path_out = Path(path_out)

    pa = io_planilhas.ler(path_a, esquema.ALIASES_USUARIO, esquema.OBRIGATORIAS_USUARIO)
    pb = io_planilhas.ler(path_b, esquema.ALIASES_EQUIPE, esquema.OBRIGATORIAS_EQUIPE)

    df_a = normalizar.aplicar(pa.df, pa.mapa, ["descricao"])
    df_b = normalizar.aplicar(pb.df, pb.mapa, ["descricao"])

    indice_clientes = mod_cliente.construir_indice(df_b, pb.mapa)
    indice_pastas = mod_pasta.construir_indice(df_b, pb.mapa)

    sugestoes: list[dict[str, Any]] = []
    contadores = {"alta": 0, "media": 0, "baixa": 0, "rev": 0, "desd": 0}

    col_desc_a = pa.mapa["descricao"]
    col_data_a = pa.mapa["data_inicio"]
    col_dur_a = pa.mapa["duracao"]
    col_exec_a = pa.mapa.get("executante")

    for _, row in df_a.iterrows():
        desc_norm = row["descricao_norm"]
        desc_orig = str(row.get(col_desc_a, "") or "")

        candidato_cliente = mod_cliente.identificar(desc_norm, indice_clientes)
        cliente_nome = candidato_cliente.nome if candidato_cliente else None

        nucleos = classificar.detectar(desc_norm)
        nucleo = classificar.nucleo_principal(nucleos)

        decisao = mod_vinculo.decidir(desc_norm, cliente_nome, df_b, pb.mapa)

        pasta_principal, pasta_alt = mod_pasta.escolher(
            cliente_nome, decisao.vinculo, desc_norm, indice_pastas,
        )

        idioma_sug = mod_idioma.detectar(pasta_principal, cliente_nome, df_b, pb.mapa)
        ts = tipo_subtipo.escolher(pasta_principal, nucleo, idioma_sug)
        desc_final, foi_reescrita = descricao.reescrever(
            nucleo, desc_orig, desc_norm, cliente_nome, idioma_sug,
        )
        flag_desd = desdobramento.detectar(desc_norm, nucleos)
        nivel, revisao = confianca.avaliar(
            candidato_cliente, decisao, pasta_principal, pasta_alt, foi_reescrita,
        )

        # Observações: agrega indícios e flags relevantes
        obs: list[str] = []
        if decisao.vinculo == esquema.VINCULO_DUVIDA and decisao.alternativa:
            obs.append(f"Dúvida vínculo; alternativa: {decisao.alternativa}")
        if pasta_alt is not None:
            obs.append(f"Pasta alternativa: {pasta_alt.numero} – {pasta_alt.nome}")
        if flag_desd:
            obs.append("Possível desdobramento em mais de uma atividade.")
        if not foi_reescrita:
            obs.append("Descrição original mantida; reescrita não pôde ser feita com segurança.")
        if pasta_principal is None:
            obs.append("Pasta não localizada na base da equipe; não foi inventada.")
        if candidato_cliente is None:
            obs.append("Cliente não identificável a partir da descrição.")

        base_comp = pasta_principal.nome if pasta_principal else (cliente_nome or "")

        sugestoes.append({
            "ID origem": row["_id_origem"],
            "Descrição original": desc_orig,
            "Descrição sugerida final": desc_final,
            "Cliente sugerido": cliente_nome or "",
            "Tipo de vínculo sugerido": decisao.vinculo,
            "Número da pasta sugerida": pasta_principal.numero if pasta_principal else "",
            "Nome da pasta sugerida": pasta_principal.nome if pasta_principal else "",
            "Tipo/Subtipo sugerido": ts,
            "Idioma sugerido": idioma_sug,
            "Data de início": _formatar_data(row.get(col_data_a)),
            "Hora de início sugerida": _hora_inicio_sugerida(),
            "Tempo total resultante": row.get(col_dur_a),
            "Duração original": row.get(col_dur_a),
            "Executante": row.get(col_exec_a) if col_exec_a else "",
            "Grau de confiança": nivel,
            "Necessita revisão humana?": revisao,
            "Indício de desdobramento?": flag_desd,
            "Observações": " | ".join(obs),
            "Base comparativa principal utilizada": base_comp,
            "Pasta alternativa plausível, se houver": (
                f"{pasta_alt.numero} – {pasta_alt.nome}" if pasta_alt else ""
            ),
        })

        contadores[nivel] += 1
        if revisao:
            contadores["rev"] += 1
        if flag_desd:
            contadores["desd"] += 1

    saida.escrever(
        caminho_saida=path_out,
        raw_usuario=pa.df,
        raw_equipe=pb.df,
        sugestoes=sugestoes,
        indice_pastas=indice_pastas,
        caminho_a=path_a,
        caminho_b=path_b,
    )

    return Resumo(
        total=len(sugestoes),
        alta=contadores["alta"],
        media=contadores["media"],
        baixa=contadores["baixa"],
        revisao_humana=contadores["rev"],
        desdobramento=contadores["desd"],
    )
