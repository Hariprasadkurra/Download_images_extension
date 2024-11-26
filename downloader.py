from fastapi import FastAPI, Form
from fastapi.responses import FileResponse, JSONResponse
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import requests
from zipfile import ZipFile
from urllib.parse import urlparse

app = FastAPI()

# Base directory for storing images
BASE_SAVE_DIR = "./images_temp"
os.makedirs(BASE_SAVE_DIR, exist_ok=True)


def extract_and_download_images(url: str) -> str:
    """
    Extract all image URLs from the webpage and download them into a zip file in a domain-based directory.
    """
    # Step 1: Parse the domain name from the URL
    parsed_url = urlparse(url)
    domain_name = parsed_url.netloc.replace("www.", "")  # Remove 'www.' for cleaner names
    save_dir = os.path.join(BASE_SAVE_DIR, f"{domain_name}_images")
    os.makedirs(save_dir, exist_ok=True)

    # Step 2: Setup Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode (no browser window)
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    # Step 3: Extract image URLs
    images = driver.find_elements(By.TAG_NAME, "img")
    image_urls = [img.get_attribute("src") for img in images if img.get_attribute("src")]
    driver.quit()

    if not image_urls:
        raise ValueError("No images found on the webpage!")

    # Step 4: Download images
    downloaded_files = []
    for i, img_url in enumerate(image_urls):
        try:
            response = requests.get(img_url, stream=True)
            if response.status_code == 200:
                file_name = f"image_{i + 1}.jpg"
                file_path = os.path.join(save_dir, file_name)
                with open(file_path, "wb") as file:
                    file.write(response.content)
                downloaded_files.append(file_path)
        except Exception as e:
            print(f"Error downloading image {img_url}: {e}")

    # Step 5: Compress images into a ZIP file
    zip_file_path = os.path.join(save_dir, "images.zip")
    with ZipFile(zip_file_path, "w") as zipf:
        for file_path in downloaded_files:
            zipf.write(file_path, os.path.basename(file_path))

    # Return the path to the ZIP file
    return zip_file_path


@app.post("/download-images/")
async def download_images(webpage_url: str = Form(...)):
    """
    API endpoint to download images from a webpage and return a zip file.
    """
    try:
        zip_path = extract_and_download_images(webpage_url)
        return FileResponse(
            path=zip_path,
            media_type="application/zip",
            filename="images.zip"
        )
    except ValueError as ve:
        return JSONResponse(content={"error": str(ve)}, status_code=400)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.get("/")
async def root():
    """
    Root endpoint with a welcome message.
    """
    return {"message": "Welcome to the FastAPI Image Downloader! Use /docs to try the API."}
