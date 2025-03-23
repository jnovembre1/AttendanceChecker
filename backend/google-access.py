from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
# Define the full drive scope for PyDrive
gauth = GoogleAuth()
gauth.settings['oauth_scope'] = ['https://www.googleapis.com/auth/drive']
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)
