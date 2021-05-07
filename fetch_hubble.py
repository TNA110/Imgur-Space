import requests
import main


def fetch_hubble_image(image_id):
    response = requests.get(f"http://hubblesite.org/api/v3/image/{image_id}", verify=False)
    response.raise_for_status()
    image_params = response.json()
    image_files = image_params.get("image_files")
    image_file = image_files[len(image_files)-1]
    image_url = "%s%s"%("http:",image_file["file_url"])
    image_extension = main.get_extension(image_url)
    filename = f"{image_id}{image_extension}"
    main.download_image(image_url, filename)