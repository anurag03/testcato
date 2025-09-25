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


## Adding Support for New LLMs

This project supports integration with various large language models (LLMs) through the `llm_provider.py` module. To add support for a new LLM provider, follow these steps:

1. **Implement the LLM Provider Interface**

   In the `llm_provider.py` file, create a new class or function that implements the interface expected by the package. This typically involves:

   - Defining how to authenticate with the LLM API (e.g., API keys, tokens).
   - Implementing methods to send prompts or requests to the LLM.
   - Handling responses and errors according to the package conventions.

2. **Register the New Provider**

   If the package uses a registry or factory pattern for LLM providers, add your new provider to the registry so it can be selected dynamically based on configuration or parameters.

3. **Configure the Package**

   Update your configuration (e.g., YAML or environment variables) to specify the new LLM provider and any necessary credentials or settings.

4. **Test the Integration**

   Write tests or run existing test suites to verify that the new provider works as expected within the package.

### Example

Here is a minimal example of adding a new LLM provider class in `llm_provider.py`:

```python
class MyNewLLMProvider:
    def __init__(self, api_key):
        self.api_key = api_key

    def send_prompt(self, prompt):
        # Implement API call to the new LLM here
        response = ...  # call API with prompt and api_key
        return response.get("text", "")
After implementing, configure your package to use MyNewLLMProvider by updating the relevant settings.

This modular design allows easy extension of supported LLMs without modifying core logic, enabling flexibility to adapt to new AI models as they become available.


---

This addition will help users and contributors understand how to extend your project with new LLM providers via the `llm_provider.py` file clearly and concisely, following best practices for README documentation[1][2][3][6].
Just now

Sonar (Recommended)

