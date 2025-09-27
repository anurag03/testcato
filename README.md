# testcato

A Python package for automatically categorizing pytest test results (passed, failed, skipped) and
enabling AI-assisted debugging of test failures.

## Install

```bash
pip install testcato
```


## Project Structure

- `testcato/` - main package directory
    - `categorizer.py` - core logic for categorizing test results
    - `llm_provider.py` - module to add support for different large language models (LLMs)
- `tests/` - unit tests for the package
- `setup.py` - package setup configuration
- `requirements.txt` - dependencies
- `LICENSE` - license file


## Features

- Automatically categorize pytest test results into structured categories like passed, failed, and skipped.
- Generate detailed JSONL reports with tracebacks for failed tests, timestamped for easy reference.
- AI-assisted debugging support for failed tests using integrated GPT models.
- Easily add support for other LLM providers via a modular llm_provider system.
- Runs seamlessly with the `--testcato` pytest option to enable enhanced test reporting.
- Configuration via an automatically created `testcato_config.yaml` file for AI agent setup.


## Usage with pytest

Run pytest with the `--testcato` flag to enable the collection and categorization of test results.

```bash
pytest --testcato
```

This will create a `testcato_result` folder in your working directory containing JSONL files with
detailed failure information.

## Configuration

The `testcato_config.yaml` file will be generated automatically when you first import or install the
package, if it doesn't already exist. Configure your AI agents here, for example:

```yaml
default: gpt

gpt:
  type: openai
  model: gpt-4
  api_key: YOUR_OPENAI_API_KEY
  api_url: https://api.openai.com/v1/chat/completions
```

Avoid committing API keys to version control; use environment variables or secret managers instead.

## Adding Support for New LLM Providers

- To add support for other large language models, implement the provider interface in `llm_provider.py`,
register your provider, and update the configuration.
- If the package uses a registry or factory pattern for LLM providers, add your new provider to the registry
so it can be selected dynamically based on configuration or parameters.

Example provider skeleton:

```python
class MyNewLLMProvider:
    def __init__(self, api_key):
        self.api_key = api_key

    def send_prompt(self, prompt):
        # Implement API call here
        response = ...  # Call API with prompt and api_key
        return response.get("text", "")
```


## Testing

Unit tests are located in the `tests/` directory. Install development dependencies and run tests using pytest:

```bash
pip install -r requirements.txt
pytest
```


## Troubleshooting

If `testcato_config.yaml` is missing or malformed, AI debugging features will be disabled. Ensure the config
file exists and is properly formatted.

When running pytest, use the `--testcato` option to enable testcato features:

```bash
pytest --testcato
```