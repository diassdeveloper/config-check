from config_check.finder import find_config_files


def test_finds_json_and_yaml_recursively(tmp_path):
    (tmp_path / "app.json").write_text("{}")
    (tmp_path / "db.yaml").write_text("a: 1")
    sub = tmp_path / "sub"
    sub.mkdir()
    (sub / "extra.yml").write_text("b: 2")

    result = find_config_files(tmp_path)

    assert result == [
        tmp_path / "app.json",
        tmp_path / "db.yaml",
        sub / "extra.yml",
    ]


def test_ignores_other_extensions(tmp_path):
    (tmp_path / "notes.txt").write_text("oi")
    (tmp_path / "script.py").write_text("print(1)")

    assert find_config_files(tmp_path) == []
