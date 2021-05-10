from urllib.parse import urlsplit
import os
import requests


def download_image(url, filename, download_path):
    filename = f"{download_path}/{filename}"
    response = requests.get(url, verify = False)
    with open(filename, "wb") as image:
        image.write(response.content)


def get_extension(url):
    splited_url = urlsplit(url)
    filepath = splited_url[2]
    filename = os.path.split(filepath)[1]
    file_extension = os.path.splitext(filename)[1]
    return file_extension
