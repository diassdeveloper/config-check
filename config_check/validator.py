def _matches_type(value: object, expected_type: type) -> bool:
    if expected_type is int and isinstance(value, bool):
        return False
    return isinstance(value, expected_type)


def validate_config(data: dict, rules: dict[str, type]) -> list[str]:
    errors: list[str] = []

    for field, expected_type in rules.items():
        if field not in data:
            errors.append(f"campo obrigatório ausente: {field}")
        elif not _matches_type(data[field], expected_type):
            errors.append(f"campo '{field}' deve ser do tipo {expected_type.__name__}")

    return errors


rules = {
    "port": int,
    "debug": bool,
}

data = {"port": 8080, "debug": True}


print(validate_config(data, rules))
