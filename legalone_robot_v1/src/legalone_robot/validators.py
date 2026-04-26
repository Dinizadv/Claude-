
from __future__ import annotations

from datetime import datetime

from .models import LaunchRow, ValidationResult


YES_VALUES = {"SIM", "S", "TRUE", "1", "Y", "YES"}
COBRAVEL_VALUES = {"SIM", "NÃO", "NAO", "N", "TRUE", "FALSE", ""}


def validate_row(row: LaunchRow, default_hora_inicio: str = "00:00") -> ValidationResult:
    errors: list[str] = []

    if row.pode_lancar.strip().upper() not in YES_VALUES:
        errors.append("linha marcada para não lançar")

    if not row.executante:
        errors.append("executante ausente")

    if not row.data_inicio:
        errors.append("data_inicio ausente")
    else:
        try:
            datetime.strptime(row.data_inicio, "%Y-%m-%d")
        except ValueError:
            errors.append("data_inicio inválida; usar YYYY-MM-DD")

    if not row.hora_inicio:
        row.hora_inicio = default_hora_inicio

    try:
        datetime.strptime(row.hora_inicio, "%H:%M")
    except ValueError:
        errors.append("hora_inicio inválida; usar HH:MM")

    if not row.duracao_hhmm:
        errors.append("duracao_hhmm ausente")
    else:
        try:
            datetime.strptime(row.duracao_hhmm, "%H:%M")
        except ValueError:
            errors.append("duracao_hhmm inválida; usar HH:MM")

    if not row.tipo_subtipo:
        errors.append("tipo_subtipo ausente")

    if not row.descricao:
        errors.append("descricao ausente")

    if row.cobravel.strip().upper() not in COBRAVEL_VALUES:
        errors.append("cobravel fora do padrão esperado")

    return ValidationResult(is_valid=not errors, errors=errors)
