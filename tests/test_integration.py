import pytest
from typing import List, Tuple
from src.simplifier import simplify_numbers


@pytest.mark.integration
def test_complex_text_transformation() -> None:
    """Test complex text with multiple number formats and types."""
    input_text = """
    Am 1. Januar 2024 um 15:30 Uhr in Raum B-123 wurden exakt 324.620,22 Euro gesammelt.
    Dabei haben 1.234,56 Menschen teilgenommen, von denen 25 Prozent unter 30 Jahre alt waren.
    Die Temperatur betrug 38,7 Grad Celsius, und 90 Prozent der Teilnehmer blieben bis zum Ende.
    """

    expected = """
    Am 1. Januar 2024 um 15:30 Uhr in Raum B-123 wurden exakt etwa 325.000 Euro gesammelt.
    Dabei haben etwa 1.000 Menschen teilgenommen, von denen jeder Vierte unter 30 Jahre alt waren.
    Die Temperatur betrug etwa 39 Grad Celsius, und fast alle der Teilnehmer blieben bis zum Ende.
    """

    result = simplify_numbers(input_text.strip())
    assert result == expected.strip()


@pytest.mark.integration
def test_mixed_format_handling() -> None:
    """Test handling of mixed number formats in the same text."""
    test_cases: List[Tuple[str, str]] = [
        (
            "Das Budget von 1,234,567.89 USD wurde in 1.234.567,89 Euro umgerechnet.",
            "Das Budget von 1,234,567.89 USD wurde in etwa 1.235.000 Euro umgerechnet.",
        ),
        (
            "Der Umsatz stieg von 1.234,56 Euro auf 2,345,678 USD.",
            "Der Umsatz stieg von etwa 1.000 Euro auf 2,345,678 USD.",
        ),
        (
            "Von den 1.234,56 Teilnehmern zahlten 50 Prozent je 99,99 Euro.",
            "Von den etwa 1.000 Teilnehmern zahlten die Hälfte je etwa 100 Euro.",
        ),
    ]

    for input_text, expected in test_cases:
        result = simplify_numbers(input_text)
        print(f"\nInput: {input_text}")
        print(f"Expected: {expected}")
        print(f"Got: {result}")
        assert result == expected


@pytest.mark.integration
def test_edge_cases_with_formats() -> None:
    """Test edge cases with different number formats."""
    test_cases: List[Tuple[str, str]] = [
        # Zero values
        ("0,00 Euro", "etwa 0 Euro"),
        ("0.00 USD", "0.00 USD"),
        # Very small values
        ("0,001 Euro", "etwa 0 Euro"),
        ("0.001 USD", "0.001 USD"),
        # Large values with mixed formats
        (
            "1.234.567,89 Euro und 9,876,543.21 USD",
            "etwa 1.235.000 Euro und 9,876,543.21 USD",
        ),
        # Multiple numbers in different formats
        (
            "Bei 38,7 Grad Celsius spendeten 1.234 Menschen je 567,89 Euro.",
            "Bei etwa 39 Grad Celsius spendeten etwa 1.000 Menschen je etwa 568 Euro.",
        ),
    ]

    for input_text, expected in test_cases:
        result = simplify_numbers(input_text)
        print(f"\nInput: {input_text}")
        print(f"Expected: {expected}")
        print(f"Got: {result}")
        assert result == expected


@pytest.mark.integration
def test_protected_patterns() -> None:
    """Test that protected patterns remain unchanged."""
    test_cases: List[Tuple[str, str]] = [
        # Dates with numbers
        (
            "Am 1. Januar 2024 waren es 1.234,56 Euro.",
            "Am 1. Januar 2024 waren es etwa 1.000 Euro.",
        ),
        # Time with numbers
        (
            "Um 15:30 Uhr wurden 1.234,56 Euro gespendet.",
            "Um 15:30 Uhr wurden etwa 1.000 Euro gespendet.",
        ),
        # Room numbers
        (
            "In Raum B-123 wurden 1.234,56 Euro gezählt.",
            "In Raum B-123 wurden etwa 1.000 Euro gezählt.",
        ),
        # Years in different contexts
        (
            "Im Jahr 2024 wurden 1.234,56 Euro gespendet.",
            "Im Jahr 2024 wurden etwa 1.000 Euro gespendet.",
        ),
    ]

    for input_text, expected in test_cases:
        result = simplify_numbers(input_text)
        print(f"\nInput: {input_text}")
        print(f"Expected: {expected}")
        print(f"Got: {result}")
        assert result == expected
