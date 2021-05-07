import requests
from urllib.parse import urlsplit
import os
import urllib3
from PIL import Image
from imgurpython import ImgurClient
from dotenv import load_dotenv
import fetch_spacex 
import fetch_hubble 


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def authenticate():
	client_id = os.environ["CLIENT_ID"]
	client_secret = os.environ['CLIENT_SECRET']
	client = ImgurClient(client_id, client_secret)
	authorization_url = client.get_auth_url('pin')
	print("Пройдите по ссылке чтобы получить пин-код: {0}".format(authorization_url))
	pin = input("Введите пин-код: ")
	credentials = client.authorize(pin, 'pin')
	client.set_user_auth(credentials['access_token'], credentials['refresh_token'])
	return client


def upload_image(client, filepath):
    print(f"Загружаю {filepath}... ")
    client.upload_from_path(filepath, anon=False)
    print("Загрузка завершена")
    print()

def download_image(url, filename):
    filename = f"images/{filename}"
    response = requests.get(url, verify = False)
    with open(filename, "wb") as image:
        image.write(response.content)


def get_extension(url):
    splited_url = urlsplit(url)
    filepath = splited_url[2]
    filename = os.path.split(filepath)[1]
    file_extension = os.path.splitext(filename)[1]
    return(file_extension)


def format_image(filename):
    image = Image.open(filename)
    image.thumbnail((1080, 1080))
    if not get_extension(filename)=="jpg":
        os.remove(filename)
        filename = filename.replace(get_extension(filename), ".jpg")
    image.save(filename, format = "JPEG")
    

def main():
    if not os.path.isdir("images"):
        os.mkdir("images")
    flight_number = int(input("Введите номер пуска, фотографиями которого вы хотите поделиться:  "))
    collection_name = (input("Введите название коллекции, которой вы хотите поделиться:  "))
    fetch_spacex.fetch_spacex_launch(flight_number)
    response = requests.get(f"http://hubblesite.org/api/v3/images/{collection_name}")
    response.raise_for_status()
    collection = response.json()
    for image in collection[:3]:
        image_id = image.get('id')
        fetch_hubble.fetch_hubble_image(image_id)
    for filename in (os.listdir("images")):
        filepath = f"images/{filename}"
        format_image(filepath)
    load_dotenv()
    client = authenticate()
    for filename in (os.listdir("images")):
        filepath = f"images/{filename}"
        upload_image(client, filepath)


if __name__==("__main__"):
    main()

