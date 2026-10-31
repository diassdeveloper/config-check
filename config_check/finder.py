from pathlib import Path

EXTENSIONS = {".json", ".yaml", ".yml"}


def find_config_files(directory: Path) -> list[Path]:
    """Devolve os arquivos de config de uma pasta e de suas subpastas."""
    return sorted(
        path
        for path in directory.rglob("*")
        if path.is_file() and path.suffix.lower() in EXTENSIONS
    )
