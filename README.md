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

When you run pytest with the `--testcato` option, a folder named `testcato_result` will be automatically created in your working directory (if it does not exist). This folder will contain JSONL files with detailed tracebacks for failed tests. Each JSONL file is named with a timestamp, e.g., `test_run_YYYYMMDD_HHMMSS.jsonl`.

## Configuration File

`testcato_config.yaml` is a configuration file for specifying AI agents and their details. It is automatically created in your working directory when you import or install the package, if not already present.

**Current AI Support:**
- Only GPT (OpenAI) models are supported for automated test result debugging.
- You must configure your GPT agent in the config file (see example below).
- The default agent should be set to your GPT agent (e.g., `default: gpt`).

**Planned Future Support:**
- Support for other AI models and providers (such as Azure, Anthropic, etc.) will be added in future releases. You can prepare additional agent sections in your config for future use.

```yaml
# default: gpt
#
# gpt:
#   type: openai
#   model: gpt-4
#   api_key: YOUR_OPENAI_API_KEY
#   api_url: https://api.openai.com/v1/chat/completions

Uncomment and edit fields as needed for your use case.
