from tools.calculator import calculator


def test_add():
    result = calculator(10, 20, "+")
    assert result == 30


def test_multiply():
    result = calculator(6, 7, "*")
    assert result == 42


def test_divide():
    result = calculator(10, 2, "/")
    assert result == 5