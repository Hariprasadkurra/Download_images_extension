**Web Image Downloader Extension with FastAPI Backend**

This project is a Chrome browser extension combined with a FastAPI backend that allows users to download all images from any webpage. Users can input a URL through the extension's interface, which communicates with the FastAPI backend to scrape and organize images from the specified page. The images are downloaded into a structured directory based on the URL structure and compressed into a ZIP file for easy access. This tool is efficient for collecting visual resources, such as photographs or graphics, for research or personal use. It eliminates the hassle of manually saving images by automating the process, providing a fast and user-friendly experience.


## File Structure
my_extension/

├── manifest.json

├── popup.html

├── popup.js

├── icon16.png

downloader.py





## Requirements

pip install fastapi uvicorn selenium requests

## To Run Code

uvicorn app:app --reload --host 0.0.0.0 --port 8000


**The API will now be accessible at http://127.0.0.1:8000**
## Chrome set up

1. Go to `chrome://extensions/`, enable **Developer mode**, and click **Load unpacked**.  
2. Select the folder containing your extension files (e.g., `manifest.json`, `popup.html`, etc.).
## 🚀 About Me
https://github.com/Hariprasadkurra
