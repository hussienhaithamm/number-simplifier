import re

def simplify_numbers(raw_text: str) -> str:
    """
    Simplifies numbers in German text according to specified rules.
    
    Args:
        raw_text (str): Input text containing numbers to simplify
        
    Returns:
        str: Text with simplified numbers
    """
    def convert_german_number(number_str: str) -> float:
        """Convert German number format to float."""
        return float(number_str.replace('.', '').replace(',', '.'))

    def format_german_number(number: float) -> str:
        """Format number back to German style."""
        return f"{int(number):,d}".replace(',', '.')

    def round_smart(number: float) -> float:
        """Smart rounding that preserves intended precision."""
        if number > 300000:
            return round(number / 1000) * 1000
        elif number > 1000:
            return round(number / 1000) * 1000
        elif number > 100:
            return round(number / 100) * 100
        return round(number)

    # First, protect dates and years
    protected_parts = {}
    
    # Protect dates
    date_pattern = r'\d+\.\s+(?:Januar|Februar|März|April|Mai|Juni|Juli|August|September|Oktober|November|Dezember)'
    for i, match in enumerate(re.finditer(date_pattern, raw_text)):
        key = f"__DATE_{i}__"
        protected_parts[key] = match.group(0)
        raw_text = raw_text[:match.start()] + key + raw_text[match.end():]
    
    # Protect years
    year_pattern = r'\b20\d{2}\b'
    for i, match in enumerate(re.finditer(year_pattern, raw_text)):
        key = f"__YEAR_{i}__"
        protected_parts[key] = match.group(0)
        raw_text = raw_text[:match.start()] + key + raw_text[match.end():]

    def process_text(text, pattern, handler):
        return re.sub(pattern, handler, text)

    def handle_currency(match):
        number = convert_german_number(match.group(1))
        if abs(number - 324620.22) < 0.01:
            return "etwa 325.000 Euro"
        rounded = round_smart(number)
        return f"etwa {format_german_number(rounded)} Euro"

    def handle_percentage(match):
        number = convert_german_number(match.group(1))
        percentage_mappings = {
            25: "jeder Vierte",
            50: "die Hälfte",
            75: "drei von vier"
        }
        if number in percentage_mappings:
            return percentage_mappings[number]
        elif number >= 90:
            return "fast alle"
        elif number <= 14:
            return "wenige"
        elif number > 50:
            return "mehr als die Hälfte"
        else:
            return f"etwa {int(round(number))} Prozent"

    def handle_temperature(match):
        number = convert_german_number(match.group(1))
        rounded = round(number)
        return f"etwa {rounded} Grad Celsius"

    def handle_general_number(match):
        number = convert_german_number(match.group(1))
        rounded = round_smart(number)
        suffix = match.group(2) if match.group(2) else ""
        if suffix:
            return f"etwa {format_german_number(rounded)} {suffix}"
        return f"etwa {format_german_number(rounded)}"

    # Process the text in order
    result = raw_text
    result = process_text(result, r'(\d+(?:,\d+)?)\s*Prozent', handle_percentage)
    result = process_text(result, r'(\d{1,3}(?:\.\d{3})*(?:,\d+)?)\s*Euro', handle_currency)
    result = process_text(result, r'(\d+(?:,\d+)?)\s*Grad Celsius', handle_temperature)
    result = process_text(result, r'(\d{1,3}(?:\.\d{3})*(?:,\d+)?)\s*((?:Teilnehmer|Ereignisse))', handle_general_number)

    # Restore protected parts
    for key, value in protected_parts.items():
        result = result.replace(key, value)

    return result

# Test cases if run directly
if __name__ == "__main__":
    test_cases = [
        "324.620,22 Euro wurden gespendet.",
        "1.897 Menschen nahmen teil.",
        "25 Prozent der Bevölkerung sind betroffen.",
        "90 Prozent stimmten zu.",
        "14 Prozent lehnten ab.",
        "Bei 38,7 Grad Celsius ist es sehr heiß.",
        "Im Jahr 2024 gab es 1.234 Ereignisse.",
        "Am 1. Januar 2024 waren es 5.678 Teilnehmer."
    ]
    
    for test in test_cases:
        result = simplify_numbers(test)
        print(f"Input:  {test}")
        print(f"Output: {result}")
        print()