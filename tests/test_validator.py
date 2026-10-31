from config_check.validator import validate_config

RULES = {
    "port": int,
    "debug": bool
}

def test_valid_date_returns() -> None:
    data = {
        "port": 8080,
        "debug": True
    }

    assert validate_config(data, RULES) == []

def test_missing_field_is_reported() -> None:
    errors = validate_config({"port": 8080}, RULES)

    assert errors == ["campo obrigatório ausente: debug"]

def test_wrong_type_is_reported() -> None:
    errors = validate_config({"port": "8080", "debug": True}, RULES)

    assert errors == ["campo 'port' deve ser do tipo int"]

def test_multiple_problems_are_all_reported() -> None:
    errors = validate_config({"port": "8080"}, RULES)

    assert len(errors) == 2


def test_bool_is_not_accepted_as_int() -> None:
    errors = validate_config({"port": True, "debug": True}, RULES)

    assert errors == ["campo 'port' deve ser do tipo int"]


def test_none_value_is_wrong_type() -> None:
    errors = validate_config({"port": None, "debug": True}, RULES)

    assert errors == ["campo 'port' deve ser do tipo int"]


def test_extra_fields_are_ignored() -> None:
    data = {"port": 8080, "debug": False, "extra": "qualquer coisa"}

    assert validate_config(data, RULES) == []