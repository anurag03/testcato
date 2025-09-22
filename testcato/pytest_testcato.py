import pytest
import os
import datetime
import xml.etree.ElementTree as ET
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
    if config.getoption("--testcato"):
        results = []
        tracebacks = []
        for report in terminalreporter.getreports("passed"):
            results.append({'name': report.nodeid, 'status': 'passed'})
        for report in terminalreporter.getreports("failed"):
            results.append({'name': report.nodeid, 'status': 'failed'})
            if hasattr(report, 'longrepr') and report.longrepr:
                tb = str(report.longrepr)
                tracebacks.append({'name': report.nodeid, 'traceback': tb})
        for report in terminalreporter.getreports("skipped"):
            results.append({'name': report.nodeid, 'status': 'skipped'})

        # Save tracebacks to XML
        if tracebacks:
            result_dir = os.path.join(os.getcwd(), 'testcato_result')
            os.makedirs(result_dir, exist_ok=True)
            root = ET.Element('TestTracebacks')
            for tb in tracebacks:
                test_elem = ET.SubElement(root, 'Test', name=tb['name'])
                tb_elem = ET.SubElement(test_elem, 'Traceback')
                tb_elem.text = tb['traceback']
            tree = ET.ElementTree(root)
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            xml_path = os.path.join(result_dir, f'test_run_{timestamp}.xml')
            tree.write(xml_path, encoding='utf-8', xml_declaration=True)
            terminalreporter.write_line(f"Tracebacks saved to {xml_path}")

        categorizer = TestCategorizer()
        categories = categorizer.categorize(results)
        terminalreporter.write_sep("-", "testcato summary")
        for category, tests in categories.items():
            terminalreporter.write_line(f"{category}:")
            for test in tests:
                terminalreporter.write_line(f"  {test}")
