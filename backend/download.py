import requests
from bs4 import BeautifulSoup
import os

# Base URL of the metadata directory
base_url = "https://the-eye.eu/public/AI/cah/laion400m-met-release/laion400m-meta/"
output_dir = "./laion400m-meta"

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Get list of files from the directory
response = requests.get(base_url)
soup = BeautifulSoup(response.text, "html.parser")

# Download each file
for link in soup.find_all("a"):
    href = link.get("href")
    if href.endswith(".parquet"):  # Only download .parquet files
        file_url = base_url + href
        print(f"Downloading {file_url}...")
        file_response = requests.get(file_url)
        with open(os.path.join(output_dir, href), "wb") as f:
            f.write(file_response.content)
