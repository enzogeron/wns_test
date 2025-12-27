from app.core.parsing_utils.money import parse_money
from app.core.parsing_utils.text import is_skippable_text


def test_is_skippable_text():
    assert is_skippable_text("") is True
    assert is_skippable_text("Precio") is True
    assert is_skippable_text("Corte") is True
    assert is_skippable_text("Carnicería") is True
    assert is_skippable_text("Tomate") is False
    
def test_parse_money_formats():
    assert parse_money("$ 6.800") == 6800
    assert parse_money("6.800") == 6800
    assert parse_money("6500") == 6500
    assert parse_money(3800) == 3800
    assert parse_money("1.234,56") == 1234.56

def test_parse_money_invalid():
    assert parse_money(None) is None
    assert parse_money("") is None
    assert parse_money("abc") is None
    assert parse_money("$") is None