import requests
import work_with_files

def fetch_spacex_launch(flight_number, download_path):
    response = requests.get(f"https://api.spacexdata.com/v3/launches/{flight_number}")
    response.raise_for_status()
    launch = response.json()
    launch_links = launch.get("links")
    image_links = launch_links.get("flickr_images")
    for image_number, image_link in enumerate(image_links):
        filename = f"spacex{image_number}.jpg"
        work_with_files.download_image(image_link, filename, download_path)