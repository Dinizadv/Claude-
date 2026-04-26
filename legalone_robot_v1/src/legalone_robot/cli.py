
from __future__ import annotations

import argparse
from .orchestrator import run_batch


def main() -> None:
    parser = argparse.ArgumentParser(description="Robô determinístico Legal One — V1")
    parser.add_argument("--input", required=True, help="Planilha XLSX/XLSM de entrada")
    parser.add_argument("--config", required=True, help="Arquivo JSON de configuração")
    parser.add_argument("--selectors", required=True, help="Arquivo JSON com seletores da UI")
    parser.add_argument("--dry-run", action="store_true", help="Somente valida a planilha")
    args = parser.parse_args()

    output = run_batch(
        input_path=args.input,
        config_path=args.config,
        selectors_path=args.selectors,
        dry_run=args.dry_run,
    )
    print(output)


if __name__ == "__main__":
    main()
