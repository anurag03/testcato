import pytest
from .categorizer import TestCategorizer

def pytest_addoption(parser):
    parser.addoption(
        "--testcato",
        action="store_true",
        default=False,
        help="Categorize test results using testcato"
    )

def pytest_terminal_summary(terminalreporter, exitstatus, config):
    if config.getoption("--testcato"):
        results = []
        for report in terminalreporter.getreports("passed"):
            results.append({'name': report.nodeid, 'status': 'passed'})
        for report in terminalreporter.getreports("failed"):
            results.append({'name': report.nodeid, 'status': 'failed'})
        for report in terminalreporter.getreports("skipped"):
            results.append({'name': report.nodeid, 'status': 'skipped'})
        categorizer = TestCategorizer()
        categories = categorizer.categorize(results)
        terminalreporter.write_sep("-", "testcato summary")
        for category, tests in categories.items():
            terminalreporter.write_line(f"{category}:")
            for test in tests:
                terminalreporter.write_line(f"  {test}")
