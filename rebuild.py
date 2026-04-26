#!/usr/bin/env python3
"""CLI: reconstruir lançamentos de horas no Legal One.

Exemplos:
    python rebuild.py --user A.xlsx --team B.xlsx --out final.xlsx
    python rebuild.py --user A.xlsx --team B.xlsx --out final.xlsx --verbose
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from reconstrutor.pipeline import reconstruir


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Reconstrói lançamentos de horas no Legal One a partir "
                    "de uma planilha incompleta e uma planilha comparativa da equipe.",
    )
    parser.add_argument("--user", required=True, help="Caminho do .xlsx com lançamentos incompletos (Arquivo A).")
    parser.add_argument("--team", required=True, help="Caminho do .xlsx comparativo da equipe (Arquivo B).")
    parser.add_argument("--out",  required=True, help="Caminho do .xlsx de saída.")
    parser.add_argument("--verbose", "-v", action="store_true", help="Imprime resumo detalhado.")
    args = parser.parse_args(argv)

    try:
        resumo = reconstruir(args.user, args.team, args.out)
    except FileNotFoundError as e:
        print(f"ERRO: {e}", file=sys.stderr)
        return 2
    except ValueError as e:
        print(f"ERRO: {e}", file=sys.stderr)
        return 3

    print(f"OK  Saída gerada: {Path(args.out).resolve()}")
    print(f"    Linhas: {resumo.total}  "
          f"(alta={resumo.alta}, media={resumo.media}, baixa={resumo.baixa})")
    print(f"    Revisão humana: {resumo.revisao_humana}  "
          f"Desdobramento sinalizado: {resumo.desdobramento}")
    if args.verbose and resumo.baixa:
        print("    Linhas em CASOS_DUVIDOSOS exigem revisão antes do uso operacional.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
