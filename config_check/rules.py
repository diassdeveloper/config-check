from pathlib import Path

from config_check.loader import ConfigLoadError, load_config

TYPE_MAP: dict[str, type] = {
    "int": int,
    "str": str,
    "bool": bool,
    "list": list,
    "dict": dict,
}

def load_rules(path: Path) -> dict[str, type]:
    raw = load_config(path)
    rules: dict[str, type] = {}
    for field, type_name in raw.items():
        if not isinstance(type_name, str) or type_name not in TYPE_MAP:
            raise ConfigLoadError(f"tipo desconhecido para '{field}': {type_name}")
        rules[field] = TYPE_MAP[type_name]
    return rules
