# testcato

A Python package for categorizing test results (passed, failed, skipped).

## Structure

- `testcato/` - main package directory
  - `categorizer.py` - core logic for categorizing test results
- `tests/` - unit tests for the package
- `setup.py` - package setup configuration
- `requirements.txt` - dependencies
- `LICENSE` - license file

categorizer = TestCategorizer()
test_results = [
    {'name': 'test_one', 'status': 'passed'},
    {'name': 'test_two', 'status': 'failed'}
]
categories = categorizer.categorize(test_results)
print(categories)
```

## Test Results Output

When you run pytest with the `--testcato` option, a folder named `testcato_result` will be automatically created in your working directory (if it does not exist). This folder will contain XML files with detailed tracebacks for failed tests. Each XML file is named with a timestamp, e.g., `test_run_YYYYMMDD_HHMMSS.xml`.

## Configuration File

`testcato_config.yaml` is a configuration file for specifying AI agents and their details. It is automatically created in your working directory when you import or install the package, if not already present. You can add multiple agents (e.g., `agent1`, `agent2`) and set a default agent:

```yaml
# default: agent1
#
# agent1:
#   type: openai
#   model: gpt-4
#   api_key: YOUR_OPENAI_API_KEY
#
# Add more agents below as agent2, agent3, etc.
# agent2:
#   type: azure
#   model: gpt-4
#   api_key: YOUR_AZURE_API_KEY
```

Uncomment and edit fields as needed for your use case.
