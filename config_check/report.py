import csv
import json
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class FileResult:
    path: str
    errors: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def write_json_report(results: list[FileResult], output: Path):
    output.parent.mkdir(parents=True, exist_ok=True)
    report = {
        "total": len(results),
        "with_errors": sum(1 for r in results if not r.ok),
        "files": [{"file": r.path, "ok": r.ok, "errors": r.errors} for r in results],
    }
    output.write_text(
        json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8"
    )


def write_csv_report(results: list[FileResult], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["file", "status", "error"])
        for r in results:
            if r.ok:
                writer.writerow([r.path, "ok", ""])
            for error in r.errors:
                writer.writerow([r.path, "error", error])
