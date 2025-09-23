# import pytest  # Unused import removed
from testcato.categorizer import TestCategorizer


def test_categorize_basic():
    categorizer = TestCategorizer()
    test_results = [
        {"name": "test_one", "status": "passed"},
        {"name": "test_two", "status": "failed"},
        {"name": "test_three", "status": "skipped"},
        {"name": "test_four", "status": "failed"},
    ]
    expected = {
        "passed": ["test_one"],
        "failed": ["test_two", "test_four"],
        "skipped": ["test_three"],
    }
    result = categorizer.categorize(test_results)
    assert result == expected


def test_categorize_empty():
    categorizer = TestCategorizer()
    test_results = []
    expected = {"passed": [], "failed": [], "skipped": []}
    result = categorizer.categorize(test_results)
    assert result == expected


def test_categorize_unknown_status():
    categorizer = TestCategorizer()
    test_results = [
        {"name": "test_one", "status": "unknown"},
        {"name": "test_two", "status": "passed"},
    ]
    expected = {"passed": ["test_two"], "failed": [], "skipped": []}
    result = categorizer.categorize(test_results)
    assert result == expected


def test_categorize_multiple_categories():
    categorizer = TestCategorizer()
    test_results = [
        {"name": "test_one", "status": "passed"},
        {"name": "test_two", "status": "failed"},
        {"name": "test_three", "status": "skipped"},
        {"name": "test_four", "status": "skipped"},
        {"name": "test_five", "status": "passed"},
    ]
    expected = {
        "passed": ["test_one", "test_five"],
        "failed": ["test_two"],
        "skipped": ["test_three", "test_four"],
    }
    result = categorizer.categorize(test_results)
    assert result == expected
