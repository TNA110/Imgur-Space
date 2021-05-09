import requests
from urllib.parse import urlsplit
import os
import urllib3
from PIL import Image
from imgurpython import ImgurClient
from dotenv import load_dotenv
import fetch_spacex 
import fetch_hubble 
import argparse


def upload_image(client, filepath):
    print(f"Загружаю {filepath}... ")
    client.upload_from_path(filepath, anon=False)
    print("Загрузка завершена")
    print()

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


def format_image(filename):
    image = Image.open(filename)
    image.thumbnail((1080, 1080))
    if not get_extension(filename) == "jpg":
        os.remove(filename)
        filename = filename.replace(get_extension(filename), ".jpg")
    image.save(filename, format = "JPEG")
    

def main():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    parser = argparse.ArgumentParser()
    parser.add_argument("download_path", nargs="?", help="В какую папку будем сохранять изображения?", default ="images")
    parser.add_argument('collection_name', nargs="?", help="Введите название коллекции, которой вы хотите поделиться", default ="news")
    parser.add_argument('flight_number', nargs="?", help="Введите номер пуска, фотографиями которого вы хотите поделиться: ", default =13)
    args = parser.parse_args()
    os.makedirs(args.download_path, exist_ok=True)
    fetch_spacex.fetch_spacex_launch(args.flight_number, args.download_path)
    fetch_hubble.fetch_hubble_image(args.collection_name,args.download_path)
    for filename in os.listdir(args.download_path):
        filepath = f"{args.download_path}/{filename}"
        format_image(filepath)
    load_dotenv()
    client_id = os.environ["CLIENT_ID"]
    client_secret = os.environ['CLIENT_SECRET']
    client = ImgurClient(client_id, client_secret)
    authorization_url = client.get_auth_url('pin')
    print("Пройдите по ссылке чтобы получить пин-код: {0}".format(authorization_url))
    pin = input("Введите пин-код: ")
    credentials = client.authorize(pin, 'pin')
    client.set_user_auth(credentials['access_token'], credentials['refresh_token'])
    for filename in (os.listdir(args.download_path)):
        filepath = f"{args.download_path}/{filename}"
        upload_image(client, filepath)

if __name__==("__main__"):
    main()