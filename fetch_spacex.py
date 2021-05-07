import requests
import main

def fetch_spacex_launch(flight_number):
    response = requests.get("https://api.spacexdata.com/v3/launches")
    response.raise_for_status()
    launches = response.json()
    launch = launches[flight_number]
    launch_links = launch.get("links")
    image_links = launch_links.get("flickr_images")
    for image_number, image_link in enumerate (image_links):
        filename = f"spacex{image_number}.jpg"
        url = image_links[image_number]
        main.download_image(url, filename)