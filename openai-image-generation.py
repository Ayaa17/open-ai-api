from dotenv import load_dotenv
from openai import OpenAI
from utils import download_image


def generate_image(_client, _prompt, _model='dall-e-3', _size='1024x1024', _quality='standard', _file_path='image.png',
                   _n=1):
    """
    The Images API provides three methods for interacting with images:
        Creating images from scratch based on a text prompt (DALL·E 3 and DALL·E 2)
        Creating edited versions of images by having the model replace some areas of a pre-existing image, based on a new text prompt (DALL·E 2 only)
        Creating variations of an existing image (DALL·E 2 only)

    :param _client: OpenAI client
    :param _prompt: prompt: A text description of the desired image(s). The maximum length is 1000
              characters for `dall-e-2` and 4000 characters for `dall-e-3`.
    :param _model: "dall-e-2", "dall-e-3"
    :param _size: "256x256", "512x512", "1024x1024", "1792x1024", "1024x1792"
    :param _quality: "standard", "hd"
    :param _file_path: output file save path, default='./image.png'
    :param _n: The number of images to generate. Must be between 1 and 10.
    :return:
    """
    response = _client.images.generate(
        model=_model,
        prompt=_prompt,
        size=_size,
        quality=_quality,
        n=_n,
    )
    image_url = response.data[0].url
    print(image_url)
    download_image(image_url, _file_path)
    return


def edit_image(_client, _image, _mask, _prompt, _size='1024x1024', _n=1, _file_path='image.png'):
    """
    Also known as "inpainting", the image edits endpoint allows you to edit or extend an image by uploading an image
    and mask indicating which areas should be replaced. The transparent areas of the mask indicate where the image
    should be edited, and the prompt should describe the full new image, not just the erased area. This endpoint can
    enable experiences like DALL·E image editing in ChatGPT Plus.

    :param _client: OpenAI client
    :param _image: The image to edit. Must be a valid PNG file, less than 4MB, and square.
    :param _mask: An additional image whose fully transparent areas (e.g. where alpha is zero)
                indicate where `image` should be edited. Must be a valid PNG file, less than
                4MB, and have the same dimensions as `image`.
                The non-transparent areas of the mask are not used when generating the output, so they don’t necessarily
                need to match the original image like the example above.
    :param _prompt: The maximum length is 1000 characters.
    :param _size: 256x256`, `512x512`, `1024x1024`
    :param _n: The number of images to generate. Must be between 1 and 10.
    :param _file_path: output file save path, default='./image.png'
    :return:
    """
    response = _client.images.edit(
        model="dall-e-2",
        image=open(_image, "rb"),  # fixme: if not file dir
        mask=open(_mask, "rb"),  # fixme: if not file dir
        prompt=_prompt,
        n=_n,
        size=_size
    )
    image_url = response.data[0].url
    print(image_url)
    download_image(image_url, _file_path)
    return


def variation_image(_client, _image, _size='1024x1024', _n=1, _file_path='image.png'):
    """
    The image variations endpoint allows you to generate a variation of a given image.
    :param _client: OpenAI client
    :param _image: Must be a valid PNG file, less than 4MB, and square
    :param _size: 256x256`, `512x512`, `1024x1024`
    :param _n: Must be between 1 and 10.
    :param _file_path:
    :return:
    """
    response = client.images.create_variation(
        model="dall-e-2",
        image=open(_image, "rb"),
        n=_n,
        size=_size
    )

    image_url = response.data[0].url
    print(image_url)
    download_image(image_url, _file_path)
    return


if __name__ == '__main__':
    load_dotenv()
    client = OpenAI()
    prompt = "a white siamese cat"
    generate_image(client, prompt)
    # edit_image(client, 'image.png', 'image-mask.png', prompt, _file_path='edit_image.png')
    # variation_image(client, 'image.png', _file_path='variation_image.png')
