import requests


def download_image(url, filename):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Throws an exception if there is a problem with the request

        with open(filename, 'wb') as f:
            f.write(response.content)

        print(f"Image has been saved to {filename}")

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")


