from pathlib import Path

import pytest

from config_check.loader import ConfigLoadError, load_config


def test_loads_valid_json(tmp_path: Path) -> None:
    file = tmp_path / "app.json"
    file.write_text('{"name": "api", "port":8080}')

    assert load_config(file) == {"name": "api", "port": 8080}


def test_loads_valid_yaml(tmp_path: Path) -> None:
    file = tmp_path / "app.yaml"
    file.write_text("name: api\nport: 8080")

    assert load_config(file) == {"name": "api", "port": 8080}


def test_empty_file_raises(tmp_path: Path) -> None:
    file = tmp_path / "vazio.json"
    file.write_text("")

    with pytest.raises(ConfigLoadError, match="vazio"):
        load_config(file)


def test_invalid_json_raises(tmp_path: Path) -> None:
    file = tmp_path / "quebrado.json"
    file.write_text("{ nome: ")

    with pytest.raises(ConfigLoadError, match="inválido"):
        load_config(file)


def test_non_dict_content_raises(tmp_path: Path) -> None:
    file = tmp_path / "lista.json"
    file.write_text("[1, 2, 3]")

    with pytest.raises(ConfigLoadError, match="objeto"):
        load_config(file)


def test_missing_file_raises(tmp_path: Path) -> None:
    with pytest.raises(ConfigLoadError):
        load_config(tmp_path / "nao_existe.json")
