from __future__ import annotations

import pytest

from legalone_robot.models import LaunchRow
from legalone_robot.validators import validate_row


def _row(**overrides) -> LaunchRow:
    base = dict(
        linha_id="1",
        executante="Joao",
        data_inicio="2026-04-26",
        hora_inicio="09:00",
        duracao_hhmm="01:30",
        tipo_subtipo="Consulta|Geral",
        descricao="Reunião com cliente",
    )
    base.update(overrides)
    return LaunchRow(**base)


def test_happy_path():
    result = validate_row(_row())
    assert result.is_valid
    assert result.errors == []


def test_blocks_when_pode_lancar_negative():
    result = validate_row(_row(pode_lancar="NAO"))
    assert not result.is_valid
    assert "linha marcada para não lançar" in result.errors


@pytest.mark.parametrize("flag", ["SIM", "S", "Sim", "TRUE", "1", "Y", "YES"])
def test_pode_lancar_accepts_truthy_values(flag):
    result = validate_row(_row(pode_lancar=flag))
    assert result.is_valid


def test_missing_executante():
    result = validate_row(_row(executante=""))
    assert not result.is_valid
    assert "executante ausente" in result.errors


def test_missing_data_inicio():
    result = validate_row(_row(data_inicio=""))
    assert not result.is_valid
    assert "data_inicio ausente" in result.errors


def test_invalid_data_inicio_format():
    result = validate_row(_row(data_inicio="26/04/2026"))
    assert not result.is_valid
    assert "data_inicio inválida; usar YYYY-MM-DD" in result.errors


def test_blank_hora_inicio_uses_default():
    row = _row(hora_inicio="")
    result = validate_row(row, default_hora_inicio="00:00")
    assert result.is_valid
    assert row.hora_inicio == "00:00"


def test_invalid_hora_inicio_format():
    result = validate_row(_row(hora_inicio="9h"))
    assert not result.is_valid
    assert "hora_inicio inválida; usar HH:MM" in result.errors


def test_missing_duracao():
    result = validate_row(_row(duracao_hhmm=""))
    assert not result.is_valid
    assert "duracao_hhmm ausente" in result.errors


def test_invalid_duracao_format():
    result = validate_row(_row(duracao_hhmm="1.5h"))
    assert not result.is_valid
    assert "duracao_hhmm inválida; usar HH:MM" in result.errors


def test_missing_tipo_subtipo():
    result = validate_row(_row(tipo_subtipo=""))
    assert not result.is_valid
    assert "tipo_subtipo ausente" in result.errors


def test_missing_descricao():
    result = validate_row(_row(descricao=""))
    assert not result.is_valid
    assert "descricao ausente" in result.errors


@pytest.mark.parametrize("value", ["SIM", "Não", "NAO", "N", "TRUE", "FALSE", ""])
def test_cobravel_accepts_known_values(value):
    result = validate_row(_row(cobravel=value))
    assert result.is_valid


def test_cobravel_rejects_unknown_value():
    result = validate_row(_row(cobravel="talvez"))
    assert not result.is_valid
    assert "cobravel fora do padrão esperado" in result.errors


def test_accumulates_multiple_errors():
    result = validate_row(_row(executante="", data_inicio="", duracao_hhmm=""))
    assert not result.is_valid
    assert len(result.errors) >= 3
    joined = result.joined_errors()
    assert "executante ausente" in joined
    assert "data_inicio ausente" in joined
    assert "duracao_hhmm ausente" in joined
