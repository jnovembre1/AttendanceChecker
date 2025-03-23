from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

# Define the scope for accessing Google Drive
SCOPES = ['https://www.googleapis.com/auth/drive']

def main():
    # Authenticate with Google Drive
    creds = None
    flow = InstalledAppFlow.from_client_secrets_file('client_secrets.json', SCOPES)
    creds = flow.run_local_server(port=0)
    
    service = build('drive', 'v3', credentials=creds)

    # Search for a folder named "LAION-Face"
    folder_name = "LAION-Face"
    query = f"mimeType='application/vnd.google-apps.folder' and name='{folder_name}' and trashed=false"
    results = service.files().list(q=query, fields="files(id, name)", supportsAllDrives=True).execute()
    folders = results.get('files', [])

    if not folders:
        print(f"No folder named '{folder_name}' found.")
        return

    folder_id = folders[0]['id']
    print(f"Folder '{folder_name}' found with ID: {folder_id}")

    # List all files in the folder
    query = f"'{folder_id}' in parents and trashed=false"
    results = service.files().list(q=query, fields="files(id, name)", supportsAllDrives=True).execute()
    items = results.get('files', [])

    if not items:
        print('No files found in the folder.')
    else:
        print('Files:')
        for item in items:
            print(f"{item['name']} ({item['id']})")

if __name__ == '__main__':
    main()
