import os
import glob

# import xml.etree.ElementTree as ET  # No longer needed, switched to JSONL
import datetime
import yaml
from .llm_providers import get_provider


def get_latest_jsonl(result_dir):
    """
    Get the latest test_run JSONL file from the result directory.

    :param result_dir: Directory containing test_run JSONL files
    :return: Latest test_run JSONL file path or None if no files are found
    """
    files = glob.glob(os.path.join(result_dir, "test_run_*.jsonl"))
    if not files:
        return None
    return max(files, key=os.path.getctime)


def load_agent_config(config_path):
    """
    Load AI agent configuration from a YAML file.

    :param config_path: Path to the YAML configuration file
    :return: Configured AI agent or None if the configuration is invalid
    """
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    if not isinstance(config, dict):
        return None
    default_agent = config.get("default", "agent1")
    agent = config.get(default_agent, {})
    # Check if agent config is empty or missing required fields
    if not agent or not agent.get("api_key") or not agent.get("api_url"):
        return None
    return agent


def send_to_ai_agent(agent, test_name, traceback):
    """
    Send a test failure to an AI agent for debugging assistance.

    :param agent: AI agent config
    :param test_name: Name of the test that failed
    :param traceback: Traceback of the test failure
    :return: Debugging response from the AI agent
    """
    try:
        provider = get_provider(agent)
        return provider.send_request(test_name, traceback)
    except ValueError as e:
        # Print error details in red to CLI for visibility
        RED = "\033[31m"
        RESET = "\033[0m"
        error_message = f"TESTCATO AI agent error for test '{test_name}': {e}"
        print(f"{RED}{error_message}{RESET}")
        return "AI agent failed to respond due to a configuration error."
    except Exception as e:
        # General exception for other issues like network errors
        RED = "\033[31m"
        RESET = "\03_3[0m"
        error_message = f"TESTCATO AI agent error for test '{test_name}': An unexpected error occurred: {e}"
        print(f"{RED}{error_message}{RESET}")
        return "AI agent failed to respond due to an unexpected error."


def debug_latest_jsonl():
    """
    Generate debug JSONL and HTML report after lines, result_dir, and timestamp are defined.

    This function loads the latest test_run JSONL file from result_dir and
    sends its tracebacks to the configured AI agent. The AI agent's responses
    are then saved to a debug JSONL file and an HTML report in result_dir.
    """
    result_dir = os.path.join(os.getcwd(), "testcato_result")
    config_path = os.path.join(os.getcwd(), "testcato_config.yaml")
    latest_jsonl = get_latest_jsonl(result_dir)
    if not latest_jsonl:
        print("No test_run JSONL file found.")
        return
    agent = load_agent_config(config_path)
    if not agent:
        # Print warning in yellow in pytest output or console
        YELLOW = "\033[33m"
        RESET = "\033[0m"
        warning_msg = f"{YELLOW}WARNING: TESTCATO: No valid AI agent config found. Debugging is disabled.{RESET}"
        import sys

        tr = getattr(sys, "_pytest_terminalreporter", None)
        if tr:
            tr.write_line(warning_msg)
        else:
            print(warning_msg)
        return
    import json

    lines = []
    with open(latest_jsonl, "r", encoding="utf-8") as f:
        for raw_line in f:
            try:
                test_data = json.loads(raw_line)
            except Exception:
                continue
            test_name = test_data.get("name") or test_data.get("test_name")
            status = test_data.get("status", "failed")
            traceback = test_data.get("traceback")
            debug_result = None
            if traceback:
                debug_result = send_to_ai_agent(agent, test_name, traceback)
            line = {
                "test_name": test_name,
                "status": status,
                "traceback": traceback,
                "debug_result": debug_result,
            }
            lines.append(line)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    debug_jsonl_path = os.path.join(result_dir, f"test_debug_{timestamp}.jsonl")
    with open(debug_jsonl_path, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(json.dumps(line, ensure_ascii=False) + "\n")
    GREEN = "\033[32m"
    RESET = "\033[0m"
    print(f"{GREEN}Debug results saved to {debug_jsonl_path}{RESET}")

    # Also generate a human-readable HTML report
    html_path = os.path.join(result_dir, f"test_debug_{timestamp}.html")
    with open(html_path, "w", encoding="utf-8") as html:
        html.write("<html><head><title>Test Debug Report</title></head><body>")
        html.write("<h1>Test Debug Report</h1>")
        html.write('<table border="1" cellpadding="5" cellspacing="0">')
        html.write(
            "<tr><th>Test Name</th><th>Status</th><th>Traceback</th><th>Debug Result</th></tr>"
        )
        for line in lines:
            html.write("<tr>")
            html.write(f'<td>{line["test_name"]}</td>')
            html.write(f'<td>{line["status"]}</td>')
            html.write(f'<td><pre>{line["traceback"]}</pre></td>')
            html.write(f'<td><pre>{line["debug_result"]}</pre></td>')
            html.write("</tr>")
        html.write("</table></body></html>")
    print(f"{GREEN}HTML debug report saved to {html_path}{RESET}")
