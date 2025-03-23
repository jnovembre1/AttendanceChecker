import os
import logging
import random
import time
from pathlib import Path

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload

# Define the scopes required for Google Drive
# Using full drive scope to ensure proper access to all files
SCOPES = ['https://www.googleapis.com/auth/drive']

def get_drive_service(token_file='token.json', client_secrets_file='client_secrets.json'):
    """
    Authenticate and build the Google Drive service.
    
    Args:
        token_file (str): Path to the token.json file
        client_secrets_file (str): Path to the client_secrets.json file
    
    Returns:
        googleapiclient.discovery.Resource: An authenticated Google Drive service
    
    Raises:
        FileNotFoundError: If client_secrets.json is not found
        Exception: If authentication fails
    """
    creds = None
    
    # Check if token file exists and load credentials
    if os.path.exists(token_file):
        try:
            creds = Credentials.from_authorized_user_file(token_file, SCOPES)
            logging.info(f"Loaded credentials from {token_file}")
        except Exception as e:
            logging.warning(f"Error loading credentials from {token_file}: {e}")
            # Backup and ignore problematic token
            backup_token = f"{token_file}.bak"
            logging.info(f"Backing up problematic token to {backup_token}")
            os.rename(token_file, backup_token)
            creds = None
    
    # Check if credentials are valid or need refresh
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                logging.info("Refreshing expired credentials")
                creds.refresh(Request())
            except Exception as e:
                logging.warning(f"Error refreshing token: {e}")
                # Force re-authentication
                creds = None
        
        # If credentials still not valid, go through authentication flow
        if not creds:
            if not os.path.exists(client_secrets_file):
                raise FileNotFoundError(
                    f"Client secrets file not found: {client_secrets_file}. "
                    "Please download it from the Google Cloud Console."
                )
            
            try:
                logging.info(f"Starting new authentication flow with {client_secrets_file}")
                flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, SCOPES)
                creds = flow.run_local_server(port=0)
                
                # Save the credentials for the next run
                with open(token_file, 'w') as token:
                    token.write(creds.to_json())
                logging.info(f"Saved new credentials to {token_file}")
            except Exception as e:
                raise Exception(f"Authentication failed: {e}")
    
    try:
        # Build and return the Drive service
        service = build('drive', 'v3', credentials=creds)
        return service
    except Exception as e:
        raise Exception(f"Failed to build Drive service: {e}")

def retry_operation(operation, max_retries=3, backoff_factor=2):
    """
    Retries a Google Drive API operation with exponential backoff on errors.
    
    Args:
        operation (callable): Function to execute
        max_retries (int): Maximum number of retry attempts
        backoff_factor (int): Factor for exponential backoff
    
    Returns:
        The result of the operation if successful
    
    Raises:
        Exception: If max retries exceeded
    """
    for attempt in range(max_retries):
        try:
            return operation()
        except HttpError as e:
            if attempt == max_retries - 1:
                # Last attempt failed, re-raise the exception
                raise
            
            logging.error(f"HttpError on attempt {attempt+1}/{max_retries}: {e}")
            sleep_time = backoff_factor ** attempt + random.uniform(0, 1)
            logging.info(f"Retrying in {sleep_time:.2f} seconds...")
            time.sleep(sleep_time)
    
    raise Exception("Max retries exceeded for operation.")

def get_folder_id(drive_service, folder_name, create_if_not_exist=False, parent_id=None):
    """
    Searches for a folder by name and returns its folder ID.
    If not found and create_if_not_exist is True, the folder is created.
    
    Args:
        drive_service: Authenticated Google Drive service
        folder_name (str): Name of the folder to find or create
        create_if_not_exist (bool): Whether to create the folder if it doesn't exist
        parent_id (str, optional): ID of the parent folder, if any
    
    Returns:
        str: ID of the found or created folder
    
    Raises:
        Exception: If folder is not found and create_if_not_exist is False
    """
    query = f"name = '{folder_name}' and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
    
    if parent_id:
        query += f" and '{parent_id}' in parents"
    
    results = drive_service.files().list(q=query, fields="files(id, name)").execute()
    items = results.get('files', [])
    
    if items:
        folder_id = items[0]['id']
        logging.info(f"Found folder '{folder_name}' with id {folder_id}")
        return folder_id
    elif create_if_not_exist:
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        
        if parent_id:
            file_metadata['parents'] = [parent_id]
        
        folder = drive_service.files().create(body=file_metadata, fields='id').execute()
        folder_id = folder.get('id')
        logging.info(f"Created folder '{folder_name}' with id {folder_id}")
        return folder_id
    else:
        raise Exception(f"Folder '{folder_name}' not found.")

def download_file(drive_service, file_id=None, file_name=None, folder_id=None, local_destination=None):
    """
    Downloads a file from Google Drive to a local destination.
    Can find file by ID directly or by name within a folder.
    
    Args:
        drive_service: Authenticated Google Drive service
        file_id (str, optional): ID of the file to download
        file_name (str, optional): Name of the file to find and download
        folder_id (str, optional): ID of the folder containing the file (if finding by name)
        local_destination (str): Path where the file should be saved
    
    Returns:
        str: Path to the downloaded file
    
    Raises:
        Exception: If file cannot be found or downloaded
    """
    if not file_id and not (file_name and folder_id):
        raise ValueError("Either file_id or both file_name and folder_id must be provided")
    
    if not local_destination:
        raise ValueError("local_destination is required")
    
    # If we only have file name and folder ID, find the file ID
    if not file_id:
        logging.info(f"Finding file '{file_name}' in folder ID {folder_id}")
        query = f"name = '{file_name}' and '{folder_id}' in parents and trashed = false"
        results = drive_service.files().list(q=query, fields="files(id, name)").execute()
        items = results.get('files', [])
        
        if not items:
            raise FileNotFoundError(f"File '{file_name}' not found in folder ID {folder_id}")
        
        file_id = items[0]['id']
    
    # Create parent directory if it doesn't exist
    local_path = Path(local_destination)
    local_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Download the file
    name_info = f"ID {file_id}" if not file_name else f"'{file_name}'"
    logging.info(f"Downloading file {name_info} to {local_destination}")
    
    request = drive_service.files().get_media(fileId=file_id)
    
    with open(local_destination, 'wb') as fh:
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            try:
                status, done = downloader.next_chunk()
                if status:
                    logging.info(f"Download {int(status.progress() * 100)}%")
            except HttpError as e:
                logging.error(f"Error during download: {e}")
                raise
    
    logging.info(f"Download complete: {local_destination}")
    return local_destination

def upload_file(drive_service, local_file, folder_id, file_name=None, mime_type=None):
    """
    Uploads a local file to the specified Google Drive folder.
    
    Args:
        drive_service: Authenticated Google Drive service
        local_file (str): Path to the local file to upload
        folder_id (str): ID of the folder where the file should be uploaded
        file_name (str, optional): Name to give the file in Drive (defaults to local file name)
        mime_type (str, optional): MIME type of the file (defaults to 'application/octet-stream')
    
    Returns:
        dict: Information about the uploaded file, including its ID
    
    Raises:
        FileNotFoundError: If the local file doesn't exist
        Exception: If the upload fails
    """
    local_path = Path(local_file)
    
    if not local_path.exists():
        raise FileNotFoundError(f"Local file not found: {local_file}")
    
    if not file_name:
        file_name = local_path.name
    
    if not mime_type:
        mime_type = 'application/octet-stream'
    
    logging.info(f"Uploading {local_file} to Google Drive folder {folder_id} as '{file_name}'")
    
    file_metadata = {
        'name': file_name,
        'parents': [folder_id]
    }
    
    media = MediaFileUpload(local_file, mimetype=mime_type)
    
    file = retry_operation(
        lambda: drive_service.files().create(
            body=file_metadata, media_body=media, fields='id,name'
        ).execute()
    )
    
    logging.info(f"Uploaded file '{file.get('name')}' with ID: {file.get('id')}")
    return file

