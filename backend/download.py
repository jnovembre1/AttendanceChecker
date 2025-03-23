import requests
from bs4 import BeautifulSoup
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import MediaIoBaseUpload
from io import BytesIO
import time
import ssl
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/drive.file']

def create_session():
    session = requests.Session()
    retry_strategy = Retry(
        total=5,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET", "POST"],
    )
    adapter = HTTPAdapter(
        max_retries=retry_strategy,
        pool_connections=10,
        pool_maxsize=10
    )
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

def main():
    creds = None
    flow = InstalledAppFlow.from_client_secrets_file('client_secrets.json', SCOPES)
    creds = flow.run_local_server(port=0)
    
    service = build('drive', 'v3', credentials=creds)
    session = create_session()

    folder_id = get_or_create_folder(service, 'LAION-Face')

    pth_file_id = check_file_exists(service, folder_id, 'laion_face_ids.pth')
    if not pth_file_id:
        upload_pth_file(service, session, folder_id)

    uploaded_files = get_uploaded_files(service, folder_id)
    max_uploaded = max(uploaded_files) if uploaded_files else -1

    base_url = "https://the-eye.eu/public/AI/cah/laion400m-met-release/laion400m-meta/"
    
    for i in range(max_uploaded + 1, 32):  # Assuming there are 32 files in total
        file_name = f"part-{str(i).zfill(5)}-5b54c5d5-bbcf-484d-a2ce-0d6f73df1a36-c000.snappy.parquet"
        if i not in uploaded_files:
            upload_parquet_file(service, session, folder_id, base_url, file_name)

    print("All files have been processed and uploaded.")

def get_or_create_folder(service, folder_name):
    query = f"mimeType='application/vnd.google-apps.folder' and name='{folder_name}'"
    results = service.files().list(q=query, fields="files(id)").execute()
    folders = results.get('files', [])
    
    if folders:
        return folders[0]['id']
    else:
        folder_metadata = {'name': folder_name, 'mimeType': 'application/vnd.google-apps.folder'}
        folder = service.files().create(body=folder_metadata, fields='id').execute()
        return folder.get('id')

def check_file_exists(service, folder_id, file_name):
    query = f"'{folder_id}' in parents and name='{file_name}'"
    results = service.files().list(q=query, fields="files(id)").execute()
    files = results.get('files', [])
    return files[0]['id'] if files else None

def get_uploaded_files(service, folder_id):
    query = f"'{folder_id}' in parents and mimeType='application/octet-stream'"
    results = service.files().list(q=query, fields="files(name)").execute()
    uploaded_files = [int(file['name'].split('-')[1].split('-')[0]) for file in results.get('files', []) if file['name'].startswith('part-')]
    return uploaded_files

def upload_pth_file(service, session, folder_id):
    pth_url = "https://huggingface.co/datasets/FacePerceiver/laion-face/resolve/main/laion_face_ids.pth"
    try:
        print(f"Downloading {pth_url}...")
        response = session.get(pth_url, timeout=(30, 300))
        response.raise_for_status()
        
        file_metadata = {'name': 'laion_face_ids.pth', 'parents': [folder_id]}
        media = MediaIoBaseUpload(
            BytesIO(response.content), 
            mimetype='application/octet-stream',
            resumable=True
        )
        
        file = service.files().create(
            body=file_metadata, 
            media_body=media, 
            fields='id'
        ).execute()
        print(f"Uploaded laion_face_ids.pth with ID: {file.get('id')}")
    except Exception as e:
        print(f"Error uploading laion_face_ids.pth: {str(e)}")

def upload_parquet_file(service, session, folder_id, base_url, href):
    file_url = base_url + href
    try:
        print(f"Downloading {file_url}...")
        file_response = session.get(file_url, timeout=(30, 300))
        file_response.raise_for_status()
        
        file_metadata = {'name': href, 'parents': [folder_id]}
        media = MediaIoBaseUpload(
            BytesIO(file_response.content), 
            mimetype='application/octet-stream',
            resumable=True
        )
        
        file = service.files().create(
            body=file_metadata, 
            media_body=media, 
            fields='id'
        ).execute()
        print(f"Uploaded {href} with ID: {file.get('id')}")
    except Exception as e:
        print(f"Error uploading {href}: {str(e)}")

if __name__ == '__main__':
    main()
