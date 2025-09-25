# testcato

A Python package for categorizing test results (passed, failed, skipped) and enabling AI-assisted 
debugging of test failures.

## Project Structure

- `testcato/` - main package directory  
  - `categorizer.py` - core logic for categorizing test results  
  - `llm_provider.py` - module to add support for different large language models (LLMs)  
- `tests/` - unit tests for the package  
- `setup.py` - package setup configuration  
- `requirements.txt` - dependencies  
- `LICENSE` - license file  

## Quick Start
```python
from testcato.categorizer import TestCategorizer

categorizer = TestCategorizer()
test_results = [    {'name': 'test_one', 'status': 'passed'},
    {'name': 'test_two', 'status': 'failed'}
]
categories = categorizer.categorize(test_results)
print(categories)
```

### Test Results Output
When running pytest with the `--testcato` option, a folder named testcato_result will be
automatically created in your working directory (if it does not exist). This folder contains JSONL
files with detailed tracebacks for failed tests. Each JSONL file is named with a timestamp, e.g.,
test_run_YYYYMMDD_HHMMSS.jsonl.

### Configuration File
The `testcato_config.yaml` file specifies AI agents and their details. It is automatically created
in your working directory when you import or install the package, if not already present.

### Current AI Support
Only GPT (OpenAI) models are supported for automated test result debugging.
You must configure your GPT agent in the config file (see example below).
The default agent should be set to your GPT agent (e.g., default: gpt).

### Planned Future Support
Support for other AI models and providers (such as Azure, Anthropic, etc.) will be added in
future releases. You can prepare additional agent sections in your config for future use.

```yaml
# default: gpt
#
# gpt:
#   type: openai
#   model: gpt-4
#   api_key: YOUR_OPENAI_API_KEY
#   api_url: https://api.openai.com/v1/chat/completions
```

### Security Tip: 
Avoid committing API keys to version control. Use environment variables or secret
managers where possible.

### Adding Support for New LLMs
This project supports integration with various large language models (LLMs) through the
llm_provider.py module. To add support for a new LLM provider, follow these steps:

### Implement the LLM Provider Interface

In the llm_provider.py file, create a new class or function that implements the interface
expected by the package. This typically involves:

Defining how to authenticate with the LLM API (e.g., API keys, tokens).
Implementing methods to send prompts or requests to the LLM.
Handling responses and errors according to the package conventions.
Register the New Provider

If the package uses a registry or factory pattern for LLM providers, add your new provider
to the registry so it can be selected dynamically based on configuration or parameters.

### Configure the Package

Update your configuration (e.g., YAML or environment variables) to specify the new LLM provider
and any necessary credentials or settings.

### Test the Integration

Write tests or run existing test suites to verify that the new provider works as expected
within the package.

### Example
```python

class MyNewLLMProvider:
    def __init__(self, api_key):
        self.api_key = api_key

    def send_prompt(self, prompt):
        # Implement API call to the new LLM here
        response = ...  # call API with prompt and api_key
        return response.get("text", "")
```

After implementing, configure your package to use MyNewLLMProvider by updating the relevant
settings.

## Running Tests
Unit tests are located in the tests/ directory. To run tests, it is recommended to use
pytest:

`pytest
Make sure to install development dependencies from requirements.txt before running tests.

## Troubleshooting & Notes
If testcato_config.yaml is missing or malformed, debugging features will be disabled.
Please ensure the config file exists and is correctly formatted.

When running pytest, use the --testcato option to enable testcato features:

`pytest --