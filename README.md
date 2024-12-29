
# Number Simplifier

## Overview
This Python program simplifies numbers in German text according to specific rules. It identifies and formats numbers, percentages, and temperatures, handling various numeric formats such as German-style (`1.234,56`) and US-style (`1,234.56`).

## Features
- Converts numbers from German and US formats to simplified representations
- Handles specialized cases:
  - Currencies (e.g., `324.620,22 Euro` → `etwa 325.000 Euro`)
  - Percentages (e.g., `25 Prozent` → `jeder Vierte`)
  - Temperatures (e.g., `38,7 Grad Celsius` → `etwa 39 Grad Celsius`)
- Protects special patterns (dates, times, room numbers) from modification
- Smart rounding based on number magnitude
- Comprehensive test suite ensuring reliability

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/number-simplifier.git
   ```
2. Navigate to the project directory:
   ```bash
   cd number-simplifier
   ```
3. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Example
```python
from src.simplifier import simplify_numbers

text = "324.620,22 Euro wurden gespendet."
result = simplify_numbers(text)
print(result)  # Output: "etwa 325.000 Euro wurden gespendet."
```

### Common Cases
```python
# Percentages
text = "25 Prozent der Bevölkerung sind betroffen."
result = simplify_numbers(text)
print(result)  # Output: "jeder Vierte der Bevölkerung sind betroffen."

# Mixed formats
text = "Bei 38,7 Grad Celsius wurden 1.234,56 Euro gespendet."
result = simplify_numbers(text)
print(result)  # Output: "Bei etwa 39 Grad Celsius wurden etwa 1.000 Euro gespendet."
```

## Number Format Handling

The library handles various formats:

1. **German Format**
   - Decimal: `1.234,56` → `etwa 1.000`
   - Large numbers: `1.234.567` → `etwa 1.235.000`

2. **US Format**
   - Decimal: `1,234.56` → `etwa 1.000`
   - Large numbers: `1,234,567` → `etwa 1.000.000`

3. **Percentage Representations**
   - 25% → "jeder Vierte"
   - 50% → "die Hälfte"
   - 75% → "drei von vier"
   - 90%+ → "fast alle"
   - ≤14% → "wenige"
   - >50% → "mehr als die Hälfte"

## Protected Patterns

The following patterns are preserved:
- Dates: `1. Januar 2024`
- Times: `15:30`
- Room numbers: `B-123`
- Years: `2024` (when not followed by units)

## Testing
Run the test suite:
```bash
pytest tests/
```

## Error Handling
The library includes robust error handling:
- Invalid input types raise `TypeError`
- Empty strings raise `ValueError`
- Invalid number formats are safely handled

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact
Submit issues through GitHub's issue tracker or contact at hussienhaitham51@gmail.com
```

