"""Configuração compartilhada de testes."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest


RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))


@pytest.fixture(scope="session")
def caminho_fixture_a() -> Path:
    p = RAIZ / "tests" / "fixtures" / "arquivo_a_demo.xlsx"
    if not p.exists():
        from tests.fixtures import gerar_fixtures
        gerar_fixtures.main()
    return p


@pytest.fixture(scope="session")
def caminho_fixture_b() -> Path:
    p = RAIZ / "tests" / "fixtures" / "arquivo_b_demo.xlsx"
    if not p.exists():
        from tests.fixtures import gerar_fixtures
        gerar_fixtures.main()
    return p
