
import os
import urllib3
import argparse

from PIL import Image
from imgurpython import ImgurClient
from dotenv import load_dotenv

import requiered_func
import fetch_spacex 
import fetch_hubble 


def upload_image(client, filepath):
    client.upload_from_path(filepath, anon=False)


def authenticate(client_id, client_secret):
    client = ImgurClient(client_id, client_secret)
    authorization_url = client.get_auth_url('pin')
    print("Пройдите по ссылке чтобы получить пин-код: {0}".format(authorization_url))
    pin = input("Введите пин-код: ")
    credentials = client.authorize(pin, 'pin')
    client.set_user_auth(credentials['access_token'], credentials['refresh_token'])
    return client


def format_image(filename):
    image = Image.open(filename)
    posting_image_size = (1080, 1080)
    image.thumbnail(posting_image_size)
    if not requiered_func.get_extension(filename) == "jpg":
        os.remove(filename)
        filename = filename.replace(requiered_func.get_extension(filename), ".jpg")
    image.save(filename, format="JPEG")
    

def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "download_path", nargs="?",
        help="В какую папку будем сохранять изображения?", 
        default="images"
    )
    parser.add_argument(
        "collection_name", nargs="?", 
        help="Введите название коллекции, которой вы хотите поделиться", 
        default="news"
    )
    parser.add_argument(
        "flight_number",
         nargs="?",
        help="Введите номер пуска, фотографиями которого вы хотите поделиться: ", 
        default=13
    )
    
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    download_path, collection_name, flight_number = args.download_path, args.collection_name, args.flight_number
    os.makedirs(download_path, exist_ok=True)
    fetch_spacex.fetch_spacex_launch(flight_number, download_path)
    fetch_hubble.fetch_hubble_image(collection_name,download_path)
    for filename in os.listdir(download_path):
        filepath = f"{download_path}/{filename}"
        format_image(filepath)
    load_dotenv()
    client_id = os.environ["CLIENT_ID"]
    client_secret = os.environ["CLIENT_SECRET"]
    client = authenticate(client_id, client_secret)
    for filename in os.listdir(download_path):
        filepath = f"{download_path}/{filename}"
        upload_image(client, filepath)


if __name__==("__main__"):
    main()