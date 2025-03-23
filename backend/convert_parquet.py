import torch
import pyarrow.parquet as pq
import pyarrow as pa
from pathlib import Path
from tqdm import tqdm
import argparse
import logging
import time
import random
import os

# Import the new google_drive_auth module
import google_drive_auth

# --- Main Processing ---
def main():
    logging.basicConfig(level=logging.INFO, 
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    
    parser = argparse.ArgumentParser(description="Filter LAION metadata Parquet files from Google Drive.")
    parser.add_argument("sample_list", help="Path to laion_face_ids.pth")
    parser.add_argument("laion_meta_dir", help="Google Drive folder name for input Parquet files")
    parser.add_argument("laion_face_meta_dir", help="Google Drive folder name for output filtered Parquet files")
    args = parser.parse_args()

    try:
        # Set up Google Drive authentication and get drive_service using the new module
        drive_service = google_drive_auth.get_drive_service()
        
        # Get folder IDs for input and output folders using the new module
        input_folder_id = google_drive_auth.get_folder_id(drive_service, args.laion_meta_dir, create_if_not_exist=False)
        output_folder_id = google_drive_auth.get_folder_id(drive_service, args.laion_face_meta_dir, create_if_not_exist=True)
    
        if not input_folder_id:
            raise FileNotFoundError(f"Input folder '{args.laion_meta_dir}' not found in Google Drive")
        
        logging.info(f"Using Google Drive folders: Input folder: {args.laion_meta_dir} (ID: {input_folder_id}), "
                    f"Output folder: {args.laion_face_meta_dir} (ID: {output_folder_id})")

        logging.info(f"Loading sample list from {args.sample_list}...")
        all_samples = torch.load(args.sample_list)

        total_filtered = 0
        # Create a unique temporary directory with timestamp to avoid conflicts
        temp_dir_name = f"temp_convert_{int(time.time())}_{random.randint(1000, 9999)}"
        temp_dir = Path(temp_dir_name)
        temp_dir.mkdir(exist_ok=True)
        logging.info(f"Created temporary directory: {temp_dir}")

        # Process each split (assumed to be 32 parts)
        for split_num in tqdm(range(32), desc="Processing splits"):
            try:
                samples = set(all_samples[split_num])
                sn = str(split_num).zfill(5)
                filename = f"part-{sn}-5b54c5d5-bbcf-484d-a2ce-0d6f73df1a36-c000.snappy.parquet"
                
                local_input_path = temp_dir / filename
                # Download file from Google Drive using the new module
                try:
                    google_drive_auth.download_file(
                        drive_service, 
                        file_name=filename, 
                        folder_id=input_folder_id, 
                        local_destination=str(local_input_path)
                    )
                
                    # Process file locally
                    logging.info(f"Processing {filename} locally...")
                    # Use context manager for table opening to ensure proper resource cleanup
                    table = pq.read_table(str(local_input_path))
                    big_table = table.to_pandas()
                    filtered_table = big_table[big_table["SAMPLE_ID"].isin(samples)]
                    logging.info(f"Found {len(filtered_table)} matching samples in {filename}")
                    
                    # Save filtered file locally
                    output_local = temp_dir / f'laion_face_part_{sn}.parquet'
                    pq.write_table(pa.Table.from_pandas(filtered_table), str(output_local))
                    
                    # Upload filtered file to Google Drive using the new module
                    google_drive_auth.upload_file(
                        drive_service, 
                        local_file=str(output_local), 
                        folder_id=output_folder_id
                    )
                    
                    total_filtered += len(filtered_table)
                    
                    # Clean up temporary files
                    if local_input_path.exists():
                        local_input_path.unlink()
                    if output_local.exists():
                        output_local.unlink()
                        
                except FileNotFoundError as e:
                    logging.warning(f"File {filename} not found in Google Drive folder '{args.laion_meta_dir}'. Skipping... Error: {e}")
                    # Verify folder exists but file is missing
                    google_drive_auth.list_files_in_folder(drive_service, input_folder_id, max_files=5)
                except Exception as e:
                    logging.error(f"Error processing file {filename}: {str(e)}")
                    # Clean up any partially created files
                    if local_input_path.exists():
                        local_input_path.unlink()
                    if output_local.exists():
                        output_local.unlink()
            except Exception as e:
                logging.error(f"Error processing split {split_num}: {str(e)}")

        logging.info(f"Processing complete. Total samples processed: {total_filtered}")

        # Clean up temporary directory after all processing is complete
        try:
            # Remove any remaining files in the temp directory
            for temp_file in temp_dir.glob('*'):
                try:
                    temp_file.unlink()
                    logging.debug(f"Removed temporary file: {temp_file}")
                except Exception as e:
                    logging.warning(f"Failed to remove temporary file {temp_file}: {str(e)}")
            
            # Remove the temporary directory
            temp_dir.rmdir()
            logging.info(f"Removed temporary directory: {temp_dir}")
        except Exception as e:
            logging.warning(f"Failed to fully clean up temporary directory {temp_dir}: {str(e)}")

    except FileNotFoundError as e:
        logging.error(f"File not found error: {str(e)}")
        logging.error("Please make sure the sample list file exists and is accessible.")
    except google_drive_auth.GoogleDriveAuthError as e:
        logging.error(f"Google Drive authentication error: {str(e)}")
        logging.error("Please check your Google API credentials and permissions.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")
        import traceback
        logging.error(traceback.format_exc())
    finally:
        # Ensure temp directory is cleaned up even if an exception occurred
        if 'temp_dir' in locals() and temp_dir.exists():
            try:
                # Try to remove any remaining files
                for temp_file in temp_dir.glob('*'):
                    try:
                        temp_file.unlink()
                    except:
                        pass
                
                # Try to remove the directory itself
                temp_dir.rmdir()
                logging.info("Cleaned up temporary directory in finally block")
            except Exception as cleanup_error:
                logging.warning(f"Failed to clean up temporary directory in finally block: {str(cleanup_error)}")

if __name__ == "__main__":
    main()
