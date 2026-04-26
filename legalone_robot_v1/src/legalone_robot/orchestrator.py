
from __future__ import annotations

import json
import os
from pathlib import Path

from .browser import LegalOneBrowser
from .excel_io import load_rows, write_results
from .logging_setup import configure_logging
from .validators import validate_row


_ENV_USUARIO = "LEGALONE_USUARIO"
_ENV_SENHA = "LEGALONE_SENHA"


def _resolve_credentials(config: dict) -> dict:
    usuario_env = os.environ.get(_ENV_USUARIO)
    senha_env = os.environ.get(_ENV_SENHA)
    if usuario_env:
        config["usuario"] = usuario_env
    if senha_env:
        config["senha"] = senha_env
    return config


def run_batch(input_path: str, config_path: str, selectors_path: str, dry_run: bool = False) -> str:
    config = json.loads(Path(config_path).read_text(encoding="utf-8"))
    selectors = json.loads(Path(selectors_path).read_text(encoding="utf-8"))
    config = _resolve_credentials(config)

    logger = configure_logging(config.get("logs_dir", "./logs"))
    rows = load_rows(input_path)
    logger.info("lote iniciado | linhas=%d | dry_run=%s", len(rows), dry_run)

    for row in rows:
        validation = validate_row(row, default_hora_inicio=config.get("default_hora_inicio", "00:00"))
        if not validation.is_valid:
            row.status_execucao = "BLOQUEADO"
            row.mensagem_retorno = validation.joined_errors()
            row.motivo_bloqueio = validation.joined_errors()
            logger.warning("linha bloqueada | linha_id=%s | motivo=%s", row.linha_id, row.motivo_bloqueio)

    if not dry_run:
        if not config.get("usuario") or not config.get("senha"):
            raise RuntimeError(
                f"Credenciais ausentes: defina {_ENV_USUARIO} e {_ENV_SENHA} ou preencha config.json"
            )
        with LegalOneBrowser(config, selectors) as browser:
            try:
                browser.login()
                logger.info("login efetuado")
            except Exception as exc:
                browser.capture_screenshot("login", "login_failure")
                logger.exception("falha no login: %s", exc)
                raise

            for row in rows:
                if row.status_execucao == "BLOQUEADO":
                    continue
                try:
                    result = browser.create_time_entry(row)
                except Exception as exc:
                    browser.capture_screenshot(row.linha_id, "exception")
                    logger.exception("exceção em linha_id=%s: %s", row.linha_id, exc)
                    row.status_execucao = "ERRO"
                    row.mensagem_retorno = f"exceção: {type(exc).__name__}: {exc}"
                    continue

                if result.ok:
                    row.status_execucao = "SUCESSO"
                    row.id_lancamento_retorno = result.launch_id
                    row.mensagem_retorno = result.message
                    logger.info("linha ok | linha_id=%s | id=%s", row.linha_id, result.launch_id)
                else:
                    row.status_execucao = "ERRO"
                    row.mensagem_retorno = result.message
                    logger.error("linha erro | linha_id=%s | msg=%s", row.linha_id, result.message)
    else:
        for row in rows:
            if not row.status_execucao:
                row.status_execucao = "VALIDADO_DRY_RUN"
                row.mensagem_retorno = "linha validada sem execução"

    output_path = str(Path(input_path).with_name(Path(input_path).stem + "_resultado.xlsx"))
    write_results(input_path, output_path, rows)
    logger.info("lote finalizado | saida=%s", output_path)
    return output_path
