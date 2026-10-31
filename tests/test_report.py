import csv
import json
from pathlib import Path

from config_check.report import FileResult, write_csv_report, write_json_report

RESULTS = [
    FileResult(path="a.json"),
    FileResult(
        path="b.json",
        errors=[
            "campo obrigatório ausente: port",
            "campo 'debug' deve ser do tipo bool",
        ],
    ),
]


def test_file_result_ok_depends_on_errors() -> None:
    assert FileResult(path="a.json").ok is True
    assert FileResult(path="b.json", errors=["x"]).ok is False


def test_json_report_content(tmp_path: Path) -> None:
    output = tmp_path / "reports" / "r.json"

    write_json_report(RESULTS, output)

    data = json.loads(output.read_text(encoding="utf-8"))
    assert data["total"] == 2
    assert data["with_errors"] == 1
    assert data["files"][0]["ok"] is True
    assert len(data["files"][1]["errors"]) == 2


def test_json_keeps_accents_readable(tmp_path: Path) -> None:
    output = tmp_path / "r.json"

    write_json_report(RESULTS, output)

    assert "obrigatório" in output.read_text(encoding="utf-8")


def test_csv_report_rows(tmp_path: Path) -> None:
    output = tmp_path / "r.csv"

    write_csv_report(RESULTS, output)

    with output.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 3
    assert rows[0]["status"] == "ok"
    assert [r["status"] for r in rows[1:]] == ["error", "error"]


def test_empty_results(tmp_path: Path) -> None:
    json_out = tmp_path / "r.json"
    csv_out = tmp_path / "r.csv"

    write_json_report([], json_out)
    write_csv_report([], csv_out)

    data = json.loads(json_out.read_text(encoding="utf-8"))
    assert data["total"] == 0
    assert data["files"] == []
    assert csv_out.read_text(encoding="utf-8").strip() == "file,status,error"
