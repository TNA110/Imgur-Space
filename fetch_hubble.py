import requests
import requiered_func

def fetch_best_quality_image(image_number, image, download_path):
        image_id = image.get("id")
        response = requests.get(f"http://hubblesite.org/api/v3/image/{image_id}", verify=False)
        response.raise_for_status()
        image_params = response.json()
        image_files = image_params.get("image_files")
        image_file = image_files[-1]
        image_url = " %s%s" % ("http:", image_file["file_url"])
        image_extension = requiered_func.get_extension(image_url)
        filename = f"{image_number}{image_id}{image_extension}"
        requiered_func.download_image(image_url, filename, download_path)

def fetch_hubble_images(collection_name, download_path):
    response = requests.get(f"http://hubblesite.org/api/v3/images/{collection_name}")
    response.raise_for_status()
    collection = response.json()
    for image_number, image in enumerate(collection):
        fetch_best_quality_image(image_number, image, download_path)
