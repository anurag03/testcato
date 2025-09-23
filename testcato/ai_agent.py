import os
import glob
import xml.etree.ElementTree as ET
import datetime
import requests
import yaml

def get_latest_jsonl(result_dir):
    files = glob.glob(os.path.join(result_dir, 'test_run_*.jsonl'))
    if not files:
        return None
    return max(files, key=os.path.getctime)

def load_agent_config(config_path):
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    if not isinstance(config, dict):
        return None
    default_agent = config.get('default', 'agent1')
    agent = config.get(default_agent, {})
    # Check if agent config is empty or missing required fields
    if not agent or not agent.get('api_key') or not agent.get('api_url'):
        return None
    return agent

def send_to_ai_agent(agent, test_name, traceback):
    api_url = agent.get('api_url')
    if not api_url:
        return "No api_url provided in agent config."
    headers = {
        'Authorization': f"Bearer {agent.get('api_key', '')}",
        'Content-Type': 'application/json'
    }
    # Payload for OpenAI chat completions API
    payload = {
        "model": agent.get('model', 'gpt-4'),
        "messages": [
            {"role": "system", "content": "You are a helpful test debugging assistant."},
            {"role": "user", "content": f"Debug this test failure: {test_name}\nTraceback:\n{traceback}"}
        ]
    }
    response = requests.post(api_url, json=payload, headers=headers)
    if response.ok:
        try:
            return response.json().get('choices', [{}])[0].get('message', {}).get('content', '')
        except Exception:
            return response.text
    # Print error details in red to CLI for visibility
    RED = '\033[31m'
    RESET = '\033[0m'
    print(f"{RED}TESTCATO AI agent error for test '{test_name}': {response.status_code} - {response.text}{RESET}")
    return "AI agent failed to respond."

def debug_latest_xml():
    # Generate debug JSONL and HTML report after lines, result_dir, and timestamp are defined
    result_dir = os.path.join(os.getcwd(), 'testcato_result')
    config_path = os.path.join(os.getcwd(), 'testcato_config.yaml')
    latest_jsonl = get_latest_jsonl(result_dir)
    if not latest_jsonl:
        print("No test_run JSONL file found.")
        return
    agent = load_agent_config(config_path)
    if not agent:
        # Print warning in yellow in pytest output or console
        YELLOW = '\033[33m'
        RESET = '\033[0m'
        warning_msg = f"{YELLOW}WARNING: TESTCATO: No valid AI agent config found. Debugging is disabled.{RESET}"
        import sys
        tr = getattr(sys, '_pytest_terminalreporter', None)
        if tr:
            tr.write_line(warning_msg)
        else:
            print(warning_msg)
        return
    import json
    lines = []
    with open(latest_jsonl, 'r', encoding='utf-8') as f:
        for raw_line in f:
            try:
                test_data = json.loads(raw_line)
            except Exception:
                continue
            test_name = test_data.get('name') or test_data.get('test_name')
            status = test_data.get('status', 'failed')
            traceback = test_data.get('traceback')
            debug_result = None
            if traceback:
                debug_result = send_to_ai_agent(agent, test_name, traceback)
            line = {
                "test_name": test_name,
                "status": status,
                "traceback": traceback,
                "debug_result": debug_result
            }
            lines.append(line)
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    debug_jsonl_path = os.path.join(result_dir, f'test_debug_{timestamp}.jsonl')
    with open(debug_jsonl_path, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(json.dumps(line, ensure_ascii=False) + '\n')
    print(f"Debug results saved to {debug_jsonl_path}")

    # Also generate a human-readable HTML report
    html_path = os.path.join(result_dir, f'test_debug_{timestamp}.html')
    with open(html_path, 'w', encoding='utf-8') as html:
        html.write('<html><head><title>Test Debug Report</title></head><body>')
        html.write('<h1>Test Debug Report</h1>')
        html.write('<table border="1" cellpadding="5" cellspacing="0">')
        html.write('<tr><th>Test Name</th><th>Status</th><th>Traceback</th><th>Debug Result</th></tr>')
        for line in lines:
            html.write('<tr>')
            html.write(f'<td>{line["test_name"]}</td>')
            html.write(f'<td>{line["status"]}</td>')
            html.write(f'<td><pre>{line["traceback"]}</pre></td>')
            html.write(f'<td><pre>{line["debug_result"]}</pre></td>')
            html.write('</tr>')
        html.write('</table></body></html>')
    print(f"HTML debug report saved to {html_path}")
