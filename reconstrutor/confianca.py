"""Avaliação de confiança da sugestão e flag de revisão humana."""

from __future__ import annotations

from .cliente import CandidatoCliente
from .esquema import CONF_ALTA, CONF_BAIXA, CONF_MEDIA, VINCULO_DUVIDA
from .pasta import CandidatoPasta
from .vinculo import DecisaoVinculo


def avaliar(
    cliente: CandidatoCliente | None,
    decisao: DecisaoVinculo,
    pasta: CandidatoPasta | None,
    pasta_alternativa: CandidatoPasta | None,
    descricao_reescrita: bool,
) -> tuple[str, bool]:
    """Retorna (nivel, revisao_humana).

    Alta:  cliente >=0.8, pasta presente, vínculo decisivo, descrição reescrita.
    Média: cliente identificado, pasta presente, demais sinais ok.
    Baixa: qualquer falha estrutural (sem cliente, sem pasta, dúvida vínculo,
           descrição não reescrita).
    """
    motivos_baixa: list[str] = []

    if cliente is None or cliente.score < 0.3:
        motivos_baixa.append("cliente_indefinido")
    if pasta is None:
        motivos_baixa.append("pasta_ausente")
    if decisao.vinculo == VINCULO_DUVIDA:
        motivos_baixa.append("vinculo_duvida")
    if not descricao_reescrita:
        motivos_baixa.append("descricao_telegrafica")

    if motivos_baixa:
        return CONF_BAIXA, True

    if cliente.score >= 0.8 and pasta_alternativa is None and decisao.vinculo != VINCULO_DUVIDA:
        return CONF_ALTA, False

    return CONF_MEDIA, False
