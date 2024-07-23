# OpenAI Library Wrapper

This project provides a simple and efficient wrapper for the OpenAI library, making it easier to interact with OpenAI's powerful models. The wrapper simplifies the process of generating text, performing completions, and other common tasks, allowing developers to integrate OpenAI's capabilities into their applications with minimal effort.

## Features
- Easy-to-use interface for interacting with OpenAI API
- Simplified text generation and completion methods
- Support for multiple OpenAI models
- Configurable parameters for custom use cases

## Installation
To install the package, use:
```bash
    pip install --upgrade openai
    pip install python-dotenv
    pip install requests
```

## Set api key
create ``.env`` in root

``` bash
#.env
# Once you add your API key below, make sure to not share it with anyone! The API key should remain private.

OPENAI_API_KEY=abc123
```

## Reference
- [open ai docs](https://platform.openai.com/docs/quickstart)
- [Aya -> open-api doc](https://ayaa17.github.io/myVitepress/ai/application/open-api.html)