
from __future__ import annotations

import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Any

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .models import LaunchRow, BrowserResult


logger = logging.getLogger("legalone_robot.browser")
_SAFE_NAME_RE = re.compile(r"[^A-Za-z0-9_-]+")


_BY_MAP = {
    "id": By.ID,
    "name": By.NAME,
    "css": By.CSS_SELECTOR,
    "xpath": By.XPATH,
}


def _locator(raw: dict[str, str]) -> tuple[str, str]:
    return _BY_MAP[raw["by"]], raw["value"]


class LegalOneBrowser:
    def __init__(self, config: dict[str, Any], selectors: dict[str, Any]) -> None:
        self.config = config
        self.selectors = selectors
        self.driver: WebDriver | None = None
        self.screenshots_dir = Path(config.get("screenshots_dir", "./screenshots"))

    def __enter__(self) -> "LegalOneBrowser":
        options = Options()
        if self.config.get("headless", False):
            options.add_argument("--headless=new")
        options.add_argument("--start-maximized")
        prefs = {
            "download.default_directory": str(Path(self.config.get("download_dir", "./downloads")).resolve()),
            "download.prompt_for_download": False,
        }
        options.add_experimental_option("prefs", prefs)
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(int(self.config.get("implicit_wait_seconds", 3)))
        self.driver.set_page_load_timeout(int(self.config.get("page_load_timeout_seconds", 30)))
        self.screenshots_dir.mkdir(parents=True, exist_ok=True)
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        if self.driver:
            self.driver.quit()
            self.driver = None

    def login(self) -> None:
        assert self.driver is not None
        self.driver.get(self.config["login_url"])
        login = self.selectors["login"]
        username = self.driver.find_element(*_locator(login["username"]))
        username.clear()
        username.send_keys(self.config["usuario"])
        password = self.driver.find_element(*_locator(login["password"]))
        password.clear()
        password.send_keys(self.config["senha"])
        self.driver.find_element(*_locator(login["submit"])).click()

    def create_time_entry(self, row: LaunchRow) -> BrowserResult:
        assert self.driver is not None
        sel = self.selectors["new_time_entry"]
        wait_form = int(self.config.get("wait_form_seconds", 10))
        wait_save = int(self.config.get("wait_after_save_seconds", 15))

        self.driver.get(self.config["new_time_entry_url"])
        WebDriverWait(self.driver, wait_form).until(
            EC.presence_of_element_located(_locator(sel["form_anchor"]))
        )

        self._set_if_present(sel, "executante", row.executante)
        self._set_if_present(sel, "data_inicio", row.data_inicio)
        self._set_if_present(sel, "hora_inicio", row.hora_inicio)
        self._set_if_present(sel, "duracao", row.duracao_hhmm)
        self._set_if_present(sel, "cliente_principal", row.cliente_principal)
        self._set_if_present(sel, "negociacao", row.negociacao)
        self._set_if_present(sel, "descricao_negociacao", row.descricao_negociacao)
        self._set_if_present(sel, "pasta", row.pasta)
        self._set_if_present(sel, "nome_pasta", row.nome_pasta)
        self._set_if_present(sel, "tipo_subtipo", row.tipo_subtipo)
        self._set_if_present(sel, "descricao", row.descricao)
        self._set_if_present(sel, "cobravel", row.cobravel)
        self._set_if_present(sel, "observacoes_executante", row.observacoes_executante)
        self._set_if_present(sel, "gerente_conta", row.gerente_conta)
        self._set_if_present(sel, "grupo", row.grupo)

        self.driver.find_element(*_locator(sel["save_button"])).click()

        error_locator = _locator(sel["error_box"])
        success_locator = _locator(sel["success_id"])

        try:
            WebDriverWait(self.driver, wait_save).until(EC.any_of(
                EC.presence_of_element_located(error_locator),
                EC.presence_of_element_located(success_locator),
            ))
        except Exception:
            self.capture_screenshot(row.linha_id, "timeout")
            return BrowserResult(ok=False, message="timeout aguardando retorno de sucesso ou erro")

        errors = self.driver.find_elements(*error_locator)
        if errors:
            text = " | ".join([e.text.strip() for e in errors if e.text.strip()])
            self.capture_screenshot(row.linha_id, "validation_error")
            return BrowserResult(ok=False, message=text or "erro de validação na tela")

        success = self.driver.find_elements(*success_locator)
        launch_id = success[0].text.strip() if success else ""
        return BrowserResult(ok=True, launch_id=launch_id, message="lançamento concluído")

    def capture_screenshot(self, linha_id: str, reason: str) -> Path | None:
        if self.driver is None:
            return None
        timestamp = datetime.now().strftime("%Y%m%dT%H%M%S")
        safe_id = _SAFE_NAME_RE.sub("_", linha_id) or "unknown"
        safe_reason = _SAFE_NAME_RE.sub("_", reason) or "error"
        path = self.screenshots_dir / f"{timestamp}_{safe_id}_{safe_reason}.png"
        try:
            self.driver.save_screenshot(str(path))
            logger.info("screenshot salvo em %s", path)
            return path
        except Exception as exc:
            logger.warning("falha ao salvar screenshot: %s", exc)
            return None

    def _set_if_present(self, sel: dict[str, Any], key: str, value: str) -> None:
        if not value:
            return
        raw = sel.get(key)
        if not raw:
            return
        element = self.driver.find_element(*_locator(raw))
        try:
            element.clear()
        except Exception:
            pass
        element.send_keys(value)
