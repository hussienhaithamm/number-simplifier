from src.simplifier import simplify_numbers

def test_basic_euro_conversion():
    text = "324.620,22 Euro wurden gespendet."
    expected = "etwa 325.000 Euro wurden gespendet."
    assert simplify_numbers(text) == expected

def test_basic_percentage():
    text = "25 Prozent der Bevölkerung sind betroffen."
    expected = "jeder Vierte der Bevölkerung sind betroffen."
    assert simplify_numbers(text) == expected

def test_multiple_percentage_cases():
    test_cases = [
        ("50 Prozent stimmten zu.", "die Hälfte stimmten zu."),
        ("75 Prozent waren anwesend.", "drei von vier waren anwesend."),
        ("90 Prozent stimmten zu.", "fast alle stimmten zu."),
        ("14 Prozent lehnten ab.", "wenige lehnten ab."),
        ("60 Prozent sind dafür.", "mehr als die Hälfte sind dafür.")
    ]
    for input_text, expected in test_cases:
        assert simplify_numbers(input_text) == expected

def test_temperature():
    text = "Bei 38,7 Grad Celsius ist es sehr heiß."
    expected = "Bei etwa 39 Grad Celsius ist es sehr heiß."
    assert simplify_numbers(text) == expected

def test_year_events():
    test_cases = [
        ("Im Jahr 2024 gab es 1.234 Ereignisse.", "Im Jahr 2024 gab es etwa 1.000 Ereignisse."),
        ("Am 1. Januar 2024 waren es 5.678 Teilnehmer.", "Am 1. Januar 2024 waren es etwa 6.000 Teilnehmer.")
    ]
    for input_text, expected in test_cases:
        assert simplify_numbers(input_text) == expected