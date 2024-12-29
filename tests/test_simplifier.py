import pytest
from src.simplifier import simplify_numbers

# Basic conversion tests
def test_basic_euro_conversion():
    text = "324.620,22 Euro wurden gespendet."
    expected = "etwa 325.000 Euro wurden gespendet."
    assert simplify_numbers(text) == expected

def test_basic_percentage():
    text = "25 Prozent der Bevölkerung sind betroffen."
    expected = "jeder Vierte der Bevölkerung sind betroffen."
    assert simplify_numbers(text) == expected

# Multiple test cases
class TestPercentages:
    def test_multiple_percentage_cases(self):
        test_cases = [
            ("50 Prozent stimmten zu.", "die Hälfte stimmten zu."),
            ("75 Prozent waren anwesend.", "drei von vier waren anwesend."),
            ("90 Prozent stimmten zu.", "fast alle stimmten zu."),
            ("14 Prozent lehnten ab.", "wenige lehnten ab."),
            ("60 Prozent sind dafür.", "mehr als die Hälfte sind dafür.")
        ]
        for input_text, expected in test_cases:
            assert simplify_numbers(input_text) == expected

    def test_special_percentage_cases(self):
        test_cases = [
            ("0 Prozent", "wenige"),
            ("100 Prozent", "fast alle"),
        ]
        for input_text, expected in test_cases:
            assert simplify_numbers(input_text) == expected

class TestNumbers:
    def test_temperature(self):
        text = "Bei 38,7 Grad Celsius ist es sehr heiß."
        expected = "Bei etwa 39 Grad Celsius ist es sehr heiß."
        assert simplify_numbers(text) == expected

    def test_year_events(self):
        test_cases = [
            ("Im Jahr 2024 gab es 1.234 Ereignisse.", "Im Jahr 2024 gab es etwa 1.000 Ereignisse."),
            ("Am 1. Januar 2024 waren es 5.678 Teilnehmer.", "Am 1. Januar 2024 waren es etwa 6.000 Teilnehmer.")
        ]
        for input_text, expected in test_cases:
            assert simplify_numbers(input_text) == expected

    def test_mixed_number_formats(self):
        text = ("Bei 38,7 Grad Celsius wurden 1.234,56 Euro gespendet, "
               "und 25 Prozent der 5.678 Teilnehmer waren zufrieden.")
        expected = ("Bei etwa 39 Grad Celsius wurden etwa 1.000 Euro gespendet, "
                   "und jeder Vierte der etwa 6.000 Teilnehmer waren zufrieden.")
        assert simplify_numbers(text) == expected

    def test_invalid_number_formats(self):
        test_cases = [
            ("123,456.789 Euro", "etwa 123.000 Euro"),
            ("1,234,567 Euro", "etwa 1.000.000 Euro"),
            ("1.234.567 Euro", "etwa 1.235.000 Euro"),
            ("1,234.567,89 Euro", "etwa 1.000 Euro"),
        ]
        for input_text, expected in test_cases:
            assert simplify_numbers(input_text) == expected

    def test_special_number_cases(self):
        test_cases = [
            ("0,0001 Euro", "etwa 0 Euro"),
            ("999.999.999 Euro", "etwa 1.000.000.000 Euro"),
        ]
        for input_text, expected in test_cases:
            assert simplify_numbers(input_text) == expected

# Error handling tests
class TestErrorHandling:
    def test_empty_input(self):
        with pytest.raises(ValueError):
            simplify_numbers("")
        with pytest.raises(ValueError):
            simplify_numbers("   ")

    def test_invalid_input_type(self):
        invalid_inputs = [None, 123, ['text'], 45.67, {'key': 'value'}]
        for invalid_input in invalid_inputs:
            with pytest.raises(TypeError):
                simplify_numbers(invalid_input)

# Edge cases
class TestEdgeCases:
    def test_no_numbers(self):
        text = "Dieser Text enthält keine Zahlen."
        assert simplify_numbers(text) == text

    def test_preserve_non_numeric(self):
        text = "Am 1. Januar 2024 um 15:30 Uhr in Raum B-123."
        expected = "Am 1. Januar 2024 um 15:30 Uhr in Raum B-123."
        assert simplify_numbers(text) == expected