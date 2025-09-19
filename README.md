# testcato

A Python package for categorizing test results (passed, failed, skipped).

## Structure

- `testcato/` - main package directory
  - `categorizer.py` - core logic for categorizing test results
- `tests/` - unit tests for the package
- `setup.py` - package setup configuration
- `requirements.txt` - dependencies
- `LICENSE` - license file

## Usage

```
from testcato.categorizer import TestCategorizer

categorizer = TestCategorizer()
test_results = [
    {'name': 'test_one', 'status': 'passed'},
    {'name': 'test_two', 'status': 'failed'}
]
categories = categorizer.categorize(test_results)
print(categories)
```
