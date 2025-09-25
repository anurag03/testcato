import requests


class BaseProvider:
    """Base class for AI providers."""

    def __init__(self, agent_config):
        self.config = agent_config

    def send_request(self, test_name, traceback):
        """
        Send a request to the AI provider.
        This method should be implemented by subclasses.
        """
        raise NotImplementedError


class OpenAIProvider(BaseProvider):
    """Provider for OpenAI models."""

    def send_request(self, test_name, traceback):
        api_url = self.config.get("api_url")
        if not api_url:
            return "No api_url provided in agent config."

        headers = {
            "Authorization": f"Bearer {self.config.get('api_key', '')}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.config.get("model", "gpt-4"),
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful test debugging assistant.",
                },
                {
                    "role": "user",
                    "content": f"Debug this test failure: {test_name}\nTraceback:\n{traceback}",
                },
            ],
        }

        response = requests.post(api_url, json=payload, headers=headers)

        if response.ok:
            try:
                return (
                    response.json()
                    .get("choices", [{}])[0]
                    .get("message", {})
                    .get("content", "")
                )
            except (IndexError, KeyError, AttributeError):
                return response.text
        else:
            # Return a more descriptive error message
            return f"API request failed with status {response.status_code}: {response.text}"


class DeepSeekProvider(OpenAIProvider):
    """Provider for DeepSeek models."""

    def send_request(self, test_name, traceback):
        # DeepSeek API is compatible with OpenAI's API format.
        # We can reuse the OpenAIProvider's logic, but with a different default model.
        self.config["model"] = self.config.get("model", "deepseek-coder")
        return super().send_request(test_name, traceback)


class AnthropicProvider(BaseProvider):
    """Provider for Anthropic models."""

    def send_request(self, test_name, traceback):
        api_url = self.config.get("api_url")
        if not api_url:
            return "No api_url provided in agent config."

        headers = {
            "x-api-key": self.config.get("api_key", ""),
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01",
        }

        payload = {
            "model": self.config.get("model", "claude-3-opus-20240229"),
            "max_tokens": 1024,
            "messages": [
                {
                    "role": "user",
                    "content": f"Debug this test failure: {test_name}\nTraceback:\n{traceback}",
                }
            ],
        }

        response = requests.post(api_url, json=payload, headers=headers)

        if response.ok:
            try:
                return response.json().get("content", [{}])[0].get("text", "")
            except (IndexError, KeyError, AttributeError):
                return response.text
        else:
            return f"API request failed with status {response.status_code}: {response.text}"


# Registry of available providers
PROVIDER_REGISTRY = {
    "openai": OpenAIProvider,
    "anthropic": AnthropicProvider,
    "deepseek": DeepSeekProvider,
    # New providers can be added here
}


def get_provider(agent_config):
    """
    Get an AI provider instance based on the agent configuration.
    """
    # Default to "openai" if no provider is specified
    provider_name = agent_config.get("provider", "openai")
    provider_class = PROVIDER_REGISTRY.get(provider_name)

    if not provider_class:
        raise ValueError(f"Unsupported provider: {provider_name}")

    return provider_class(agent_config)
