import re
import pytest
import os
import datetime
## import xml.etree.ElementTree as ET  # No longer needed, switched to JSONL
from .categorizer import TestCategorizer

def pytest_addoption(parser):
    parser.addoption(
        "--testcato",
        action="store_true",
        default=False,
        help="Categorize test results using testcato"
    )

def pytest_configure(config):
    if config.getoption("--testcato"):
        # Add -vvv for maximum verbosity if not already present
        # Pytest config.option.verbose is an int, 0=default, 1=-v, 2=-vv, 3=-vvv
        if getattr(config.option, "verbose", 0) < 3:
            config.option.verbose = 3

def pytest_terminal_summary(terminalreporter, exitstatus, config):
    def remove_ansi_codes(text):
        ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
        return ansi_escape.sub('', text)
    if config.getoption("--testcato"):
        results = []
        tracebacks = []
        for report in terminalreporter.getreports("passed"):
            results.append({'name': report.nodeid, 'status': 'passed'})
        for report in terminalreporter.getreports("failed"):
            results.append({'name': report.nodeid, 'status': 'failed'})
            if hasattr(report, 'longrepr') and report.longrepr:
                tb = remove_ansi_codes(str(report.longrepr))
                tracebacks.append({'name': report.nodeid, 'traceback': tb})
        for report in terminalreporter.getreports("skipped"):
            results.append({'name': report.nodeid, 'status': 'skipped'})

        # Save tracebacks to JSON Lines
        if tracebacks:
            import json
            result_dir = os.path.join(os.getcwd(), 'testcato_result')
            os.makedirs(result_dir, exist_ok=True)
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            jsonl_path = os.path.join(result_dir, f'test_run_{timestamp}.jsonl')
            with open(jsonl_path, 'w', encoding='utf-8') as f:
                for tb in tracebacks:
                    f.write(json.dumps(tb, ensure_ascii=False) + '\n')
            terminalreporter.write_line(f"Tracebacks saved to {jsonl_path}")

        categorizer = TestCategorizer()
        categories = categorizer.categorize(results)
        terminalreporter.write_sep("-", "testcato summary")
        for category, tests in categories.items():
            terminalreporter.write_line(f"{category}:")
            for test in tests:
                terminalreporter.write_line(f"  {test}")

    # Automatically send latest JSONL to AI agent and save debug file
        try:
            from .ai_agent import debug_latest_jsonl
            debug_latest_jsonl()
        except Exception as e:
            terminalreporter.write_line(f"Error sending JSONL to AI agent: {e}")
