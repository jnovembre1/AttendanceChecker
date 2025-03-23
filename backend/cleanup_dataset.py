#!/usr/bin/env python
"""
cleanup_dataset.py - A script to clean up datasets by keeping only specific subset files.

This script:
1. Takes a directory path as input
2. Keeps only the files corresponding to the specified subsets [0, 2, 5, 8, 13, 15, 17, 18, 21, 22, 24, 25, 28]
3. Deletes all other files
4. Includes proper error handling and confirmation
"""

import os
import re
import sys
import argparse
import logging
import pprint
from pathlib import Path

# Import Google Drive authentication module
from google_drive_auth import get_drive_service, get_folder_id

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Clean up dataset by keeping only specified subset files."
    )
    parser.add_argument(
        "directory", 
        type=str, 
        help="Directory path containing the dataset files"
    )
    parser.add_argument(
        "--dry-run", 
        action="store_true", 
        help="Show what would be deleted without actually deleting"
    )
    parser.add_argument(
        "--no-confirm", 
        action="store_true", 
        help="Skip confirmation prompt"
    )
    return parser.parse_args()


def get_part_number(filename):
    """
    Extract part number from filename if it matches the expected pattern.
    
    Expected pattern examples:
    - laion_face_part_00000.parquet
    - laion_face_part_00015.parquet
    """
    # More specific regex pattern to match LAION dataset files
    pattern = r'laion_face_part_(\d{5})\.parquet'
    
    logging.debug(f"Attempting to match filename: {filename}")
    match = re.search(pattern, filename)
    
    if match:
        part_num = int(match.group(1))
        logging.debug(f"Match found! Part number: {part_num}")
        return part_num
    
    logging.debug(f"No match found for filename: {filename}")
    return None


def cleanup_directory(directory_path, subsets, dry_run=False, skip_confirm=False):
    """
    Clean up the Google Drive directory by keeping only files corresponding to specified subsets.
    
    Args:
        directory_path: Path/name of the Google Drive folder containing the dataset files
        subsets: List of subset numbers to keep
        dry_run: If True, only show what would be deleted without deleting
        skip_confirm: If True, skip confirmation prompt
    
    Returns:
        tuple: (Number of files kept, Number of files deleted)
    """
    try:
        # Set debug logging if needed
        if dry_run:
            logging.getLogger().setLevel(logging.DEBUG)
            logging.debug("Debug logging enabled")
            
        # Initialize Google Drive service
        logging.info("Initializing Google Drive service...")
        drive_service = get_drive_service()
        
        # Get folder ID for the specified folder
        try:
            logging.info(f"Finding folder ID for '{directory_path}'...")
            folder_id = get_folder_id(drive_service, directory_path, create_if_not_exist=False)
            logging.info(f"Found folder ID: {folder_id}")
        except Exception as e:
            print(f"Error: Google Drive folder '{directory_path}' not found: {e}")
            return 0, 0
        
        # List all files in the Google Drive folder
        logging.info(f"Listing files in folder '{directory_path}'...")
        query = f"'{folder_id}' in parents and trashed = false and mimeType != 'application/vnd.google-apps.folder'"
        results = drive_service.files().list(
            q=query,
            fields="files(id, name)"
        ).execute()
        
        all_files = results.get('files', [])
        logging.info(f"Found {len(all_files)} files in Google Drive folder")
        
        if dry_run:
            logging.debug("File list from Google Drive:")
            for i, file_item in enumerate(all_files):
                logging.debug(f"  {i+1}. {file_item['name']}")
        
        # Separate files to keep and delete
        files_to_keep = []
        files_to_delete = []
        
        for file_item in all_files:
            file_name = file_item['name']
            file_id = file_item['id']
            part_number = get_part_number(file_name)
            
            if part_number is not None:
                if part_number in subsets:
                    logging.info(f"Keeping file '{file_name}' - part number {part_number} is in subset list")
                    files_to_keep.append(file_item)
                else:
                    logging.info(f"Marking file '{file_name}' for deletion - part number {part_number} is not in subset list")
                    files_to_delete.append(file_item)
            else:
                # If not matching our pattern, we'll keep it to be safe
                logging.info(f"Keeping file '{file_name}' - does not match part file pattern")
                files_to_keep.append(file_item)
        
        # Show summary
        print(f"\nFound {len(all_files)} files in Google Drive folder '{directory_path}'")
        print(f"Files to keep: {len(files_to_keep)}")
        print(f"Files to delete: {len(files_to_delete)}")
        
        # Print pattern matching statistics in dry run mode
        if dry_run:
            matched_parts = [get_part_number(f['name']) for f in all_files]
            valid_parts = [p for p in matched_parts if p is not None]
            print(f"\nPattern matching statistics:")
            print(f"  - Total files: {len(all_files)}")
            print(f"  - Files with valid part numbers: {len(valid_parts)}")
            print(f"  - Unique part numbers found: {sorted(set(valid_parts))}")
            print(f"  - Files without valid part numbers: {len(all_files) - len(valid_parts)}")
        
        if len(files_to_delete) == 0:
            print("No files to delete. Exiting.")
            return len(files_to_keep), 0
        
        # Show files to be deleted
        print("\nFiles to be deleted:")
        for file_item in files_to_delete:
            part_num = get_part_number(file_item['name'])
            print(f"  - {file_item['name']} (Part: {part_num}, ID: {file_item['id']})")
        
        # Confirm deletion
        if not dry_run and not skip_confirm:
            confirm = input("\nAre you sure you want to delete these files from Google Drive? (yes/no): ")
            if confirm.lower() != "yes":
                print("Operation cancelled.")
                return len(files_to_keep), 0
        
        # Delete files from Google Drive
        deleted_count = 0
        for file_item in files_to_delete:
            file_name = file_item['name']
            file_id = file_item['id']
            part_num = get_part_number(file_name)
            
            if dry_run:
                print(f"Would delete from Google Drive: {file_name} (Part: {part_num}, ID: {file_id})")
            else:
                try:
                    # Delete the file from Google Drive
                    drive_service.files().delete(fileId=file_id).execute()
                    deleted_count += 1
                    print(f"Deleted from Google Drive: {file_name}")
                except Exception as e:
                    print(f"Error deleting file from Google Drive {file_name}: {e}")
        
        if dry_run:
            print(f"\nDry run completed. Would have deleted {len(files_to_delete)} files from Google Drive.")
        else:
            print(f"\nCleanup completed. Deleted {deleted_count} files, kept {len(files_to_keep)} files in Google Drive.")
        
        return len(files_to_keep), deleted_count
    except Exception as e:
        print(f"Error during cleanup: {e}")
        return 0, 0


def main():
    """Main function."""
    # Subsets to keep based on requirement
    subsets_to_keep = [0, 2, 5, 8, 13, 15, 17, 18, 21, 22, 24, 25, 28]
    
    # Parse arguments
    args = parse_arguments()
    
    print(f"Cleaning up dataset in Google Drive folder: {args.directory}")
    print(f"Keeping only subsets: {subsets_to_keep}")
    
    if args.dry_run:
        print("DRY RUN MODE: No files will be deleted from Google Drive")
        print("Debug logging enabled to show file pattern matching details")
    
    # Clean up directory
    kept, deleted = cleanup_directory(
        args.directory, 
        subsets_to_keep, 
        dry_run=args.dry_run,
        skip_confirm=args.no_confirm
    )
    
    if not args.dry_run:
        print(f"\nSummary: Kept {kept} files, deleted {deleted} files.")
    

if __name__ == "__main__":
    main()

