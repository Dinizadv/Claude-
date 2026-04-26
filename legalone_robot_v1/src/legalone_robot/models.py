
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class LaunchRow:
    linha_id: str
    executante: str
    data_inicio: str
    hora_inicio: str
    duracao_hhmm: str
    cliente_principal: str = ""
    negociacao: str = ""
    descricao_negociacao: str = ""
    pasta: str = ""
    nome_pasta: str = ""
    tipo_subtipo: str = ""
    descricao: str = ""
    cobravel: str = ""
    observacoes_executante: str = ""
    gerente_conta: str = ""
    grupo: str = ""
    pode_lancar: str = "SIM"
    motivo_bloqueio: str = ""
    status_execucao: str = ""
    id_lancamento_retorno: str = ""
    mensagem_retorno: str = ""

    def to_result_dict(self) -> dict:
        return {
            "linha_id": self.linha_id,
            "status_execucao": self.status_execucao,
            "id_lancamento_retorno": self.id_lancamento_retorno,
            "mensagem_retorno": self.mensagem_retorno,
        }


@dataclass
class ValidationResult:
    is_valid: bool
    errors: List[str] = field(default_factory=list)

    def joined_errors(self) -> str:
        return " | ".join(self.errors)


@dataclass
class BrowserResult:
    ok: bool
    launch_id: str = ""
    message: str = ""
