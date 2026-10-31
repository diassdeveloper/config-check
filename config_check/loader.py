import json
from pathlib import Path

import yaml


class ConfigLoadError(Exception):
    """Erro ao ler ou interpretar um arquivo de configuração."""


def load_config(path: Path) -> dict:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise ConfigLoadError(f"não foi possível ler o arquivo: {exc}") from exc

    if not text.strip():
        raise ConfigLoadError("Arquivo vazio.")

    try:
        if path.suffix.lower() == ".json":
            data = json.loads(text)
        else:
            data = yaml.safe_load(text)
    except (json.JSONDecodeError, yaml.YAMLError) as exc:
        raise ConfigLoadError(f"conteúdo inválido: {exc}") from exc

    if not isinstance(data, dict):
        raise ConfigLoadError("o conteúdo deve ser um objeto (chave: valor)")

    return data
