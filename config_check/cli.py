import argparse
import sys
from pathlib import Path

from config_check.finder import find_config_files
from config_check.loader import ConfigLoadError, load_config
from config_check.report import FileResult, write_csv_report, write_json_report
from config_check.rules import load_rules
from config_check.validator import validate_config


def check_directory(directory: Path, rules: dict[str, type]) -> list[FileResult]:
    results: list[FileResult] = []
    for path in find_config_files(directory):
        try:
            errors = validate_config(load_config(path), rules)
        except ConfigLoadError as exc:
            errors = [str(exc)]
        results.append(FileResult(path=str(path), errors=errors))
    return results

def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="config-check",
        description="Valida arquivos JSON/YAML de configuração.",
    )
    parser.add_argument("directory", type=Path, help="pasta com as configs")
    parser.add_argument("--rules", type=Path, required=True, help="YAML com as regras")
    parser.add_argument("--output", type=Path, default=Path("reports"), help="pasta do relatório")
    return parser.parse_args(argv)

def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    if not args.directory.is_dir():
        print(f"erro: pasta não encontrada: {args.directory}", file=sys.stderr)
        return 2
    try:
        rules = load_rules(args.rules)
    except ConfigLoadError as exc:
        print(f"erro nas regras: {exc}", file=sys.stderr)
        return 2

    results = check_directory(args.directory, rules)
    write_json_report(results, args.output / "report.json")
    write_csv_report(results, args.output / "report.csv")

    failed = sum(1 for r in results if not r.ok)
    print(f"{len(results)} arquivo(s) verificado(s), {failed} com erro")
    return 1 if failed else 0