import os
import glob
import xml.etree.ElementTree as ET
import datetime
import requests
import yaml

def get_latest_xml(result_dir):
    files = glob.glob(os.path.join(result_dir, 'test_run_*.xml'))
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
    # The payload structure should be defined by the user in their config and usage
    payload = {
        "test_name": test_name,
        "traceback": traceback
    }
    response = requests.post(api_url, json=payload, headers=headers)
    if response.ok:
        return response.text
    return "AI agent failed to respond."

def debug_latest_xml():
    result_dir = os.path.join(os.getcwd(), 'testcato_result')
    config_path = os.path.join(os.getcwd(), 'testcato_config.yaml')
    latest_xml = get_latest_xml(result_dir)
    if not latest_xml:
        print("No test_run XML file found.")
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
    tree = ET.parse(latest_xml)
    root = tree.getroot()
    lines = []
    for test_elem in root.findall('Test'):
        name = test_elem.get('name')
        tb_elem = test_elem.find('Traceback')
        debug_result = None
        if tb_elem is not None:
            debug_result = send_to_ai_agent(agent, name, tb_elem.text)
        line = {
            "name": name,
            "traceback": tb_elem.text if tb_elem is not None else None,
            "debug": debug_result
        }
        lines.append(line)
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    debug_jsonl_path = os.path.join(result_dir, f'test_debugg_{timestamp}.jsonl')
    with open(debug_jsonl_path, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(json.dumps(line, ensure_ascii=False) + '\n')
    print(f"Debug results saved to {debug_jsonl_path}")
