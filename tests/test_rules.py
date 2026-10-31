from pathlib import Path

import pytest

from config_check.loader import ConfigLoadError
from config_check.rules import load_rules


def test_maps_type_names(tmp_path: Path) -> None:
    file = tmp_path / "rules.yaml"
    file.write_text("port: int\nname: str\n")

    assert load_rules(file) == {"port": int, "name": str} 

def test_unknown_type_raises(tmp_path: Path) -> None:
    file = tmp_path / "rules.yaml"
    file.write_text("port: inteiro\n")

    with pytest.raises(ConfigLoadError, match="inteiro"):
        load_rules(file)
        