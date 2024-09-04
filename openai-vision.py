from dotenv import load_dotenv
from openai import OpenAI
import base64


def understand_image(_client, _input_url, ):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "What’s in this image?"},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": _input_url,
                        },
                    },
                ],
            }
        ],
        max_tokens=10,
    )
    print(response.choices[0])
    return


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


if __name__ == '__main__':
    load_dotenv()
    client = OpenAI()
    # sample_image = """https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"""
    image_dir = 'demo\\image.png'
    base64_url = f"data:image/jpeg;base64,{encode_image(image_dir)}"
    print(base64_url)
    understand_image(client, base64_url)
