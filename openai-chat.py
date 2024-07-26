from dotenv import load_dotenv
from openai import OpenAI


def chat(_client, _message, _model="gpt-4o-mini"):
    response = client.chat.completions.create(
        model=_model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": _message}
        ]
    )

    print(response.choices[0].message.content)


if __name__ == '__main__':
    load_dotenv()
    client = OpenAI()
    input_text = "What is a LLM?"
    chat(client, input_text)
