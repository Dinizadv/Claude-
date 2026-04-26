
from __future__ import annotations

import json
from pathlib import Path

from .browser import LegalOneBrowser
from .excel_io import load_rows, write_results
from .validators import validate_row


def run_batch(input_path: str, config_path: str, selectors_path: str, dry_run: bool = False) -> str:
    config = json.loads(Path(config_path).read_text(encoding="utf-8"))
    selectors = json.loads(Path(selectors_path).read_text(encoding="utf-8"))
    rows = load_rows(input_path)

    for row in rows:
        validation = validate_row(row, default_hora_inicio=config.get("default_hora_inicio", "00:00"))
        if not validation.is_valid:
            row.status_execucao = "BLOQUEADO"
            row.mensagem_retorno = validation.joined_errors()
            row.motivo_bloqueio = validation.joined_errors()

    if not dry_run:
        with LegalOneBrowser(config, selectors) as browser:
            browser.login()
            for row in rows:
                if row.status_execucao == "BLOQUEADO":
                    continue
                result = browser.create_time_entry(row)
                if result.ok:
                    row.status_execucao = "SUCESSO"
                    row.id_lancamento_retorno = result.launch_id
                    row.mensagem_retorno = result.message
                else:
                    row.status_execucao = "ERRO"
                    row.mensagem_retorno = result.message
    else:
        for row in rows:
            if not row.status_execucao:
                row.status_execucao = "VALIDADO_DRY_RUN"
                row.mensagem_retorno = "linha validada sem execução"

    output_path = str(Path(input_path).with_name(Path(input_path).stem + "_resultado.xlsx"))
    write_results(input_path, output_path, rows)
    return output_path
