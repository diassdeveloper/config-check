from pathlib import Path

from config_check.cli import main


def make_configs(tmp_path: Path) -> Path:
    configs = tmp_path / "configs"
    configs.mkdir()
    return configs


def run(tmp_path: Path, configs: Path, rules_text: str = "port: int\ndebug: bool\n") -> int:
    rules = tmp_path / "rules.yaml"
    rules.write_text(rules_text)
    out = tmp_path / "out"
    return main([str(configs), "--rules", str(rules), "--output", str(out)])


def test_exit_0_when_all_valid(tmp_path: Path) -> None:
    configs = make_configs(tmp_path)
    (configs / "ok.json").write_text('{"port": 8080, "debug": false}')

    assert run(tmp_path, configs) == 0
    assert (tmp_path / "out" / "report.json").exists()
    assert (tmp_path / "out" / "report.csv").exists()


def test_exit_1_when_config_is_invalid(tmp_path: Path) -> None:
    configs = make_configs(tmp_path)
    (configs / "bad.json").write_text('{"port": "8080", "debug": false}')

    assert run(tmp_path, configs) == 1


def test_exit_1_when_file_is_broken(tmp_path: Path) -> None:
    configs = make_configs(tmp_path)
    (configs / "quebrado.json").write_text("{ nome: ")

    assert run(tmp_path, configs) == 1


def test_exit_2_when_directory_missing(tmp_path: Path) -> None:
    assert run(tmp_path, tmp_path / "nao_existe") == 2


def test_exit_2_when_rules_have_unknown_type(tmp_path: Path) -> None:
    configs = make_configs(tmp_path)

    assert run(tmp_path, configs, rules_text="port: inteiro\n") == 2