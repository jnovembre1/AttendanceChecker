import torch
import pyarrow.parquet as pq
import pyarrow as pa
import os
from tqdm import tqdm
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("sample_list", help="Path to laion_face_ids.pth")
    parser.add_argument("laion_meta_dir", help="Directory containing Parquet metadata files")
    parser.add_argument("laion_face_meta_dir", help="Output directory for filtered Parquet files")
    args = parser.parse_args()

    all_count = 0
    laion_meta_dir = args.laion_meta_dir
    laion_face_meta_dir = args.laion_face_meta_dir

    # Load sample list (torch format)
    print(f"Loading sample list from {args.sample_list}...")
    all_samples = torch.load(args.sample_list)

    # Ensure output directory exists
    os.makedirs(laion_face_meta_dir, exist_ok=True)

    # Process each Parquet file in chunks
    for split_num in tqdm(range(32)):
        try:
            samples = set(all_samples[split_num])
            sn = str(split_num).zfill(5)
            big_parquet_file = os.path.join(laion_meta_dir, f"part-{sn}-5b54c5d5-bbcf-484d-a2ce-0d6f73df1a36-c000.snappy.parquet")

            if not os.path.exists(big_parquet_file):
                print(f"File not found: {big_parquet_file}. Skipping...")
                continue

            # Read Parquet file and filter rows with faces
            big_table = pq.read_table(big_parquet_file).to_pandas()
            big_table["has_face"] = big_table["SAMPLE_ID"].map(lambda x: x in samples)
            filtered_table = big_table[big_table["has_face"]]
            del filtered_table["has_face"]

            # Save filtered data to output directory
            output_file = os.path.join(laion_face_meta_dir, f'laion_face_part_{sn}.parquet')
            pq.write_table(pa.Table.from_pandas(filtered_table), output_file)

            all_count += len(filtered_table)
        except Exception as e:
            print(f"Error processing split {split_num}: {e}")

    print(f"Processing complete. Total samples processed: {all_count}")
