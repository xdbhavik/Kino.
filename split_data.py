import pickle
import numpy as np
import os

def compress_and_split():
    # 1. Load the giant 600MB file
    print("Loading original file (this might take a moment)...")
    try:
        similarity = pickle.load(open('similarity.pkl', 'rb'))
    except FileNotFoundError:
        print("Error: similarity.pkl not found!")
        return

    # 2. Compress to float16 (Reduces size by 75%)
    print("Compressing to float16...")
    similarity_small = similarity.astype(np.float16)

    # 3. Save the compressed version temporarily
    compressed_filename = 'similarity_compressed.pkl'
    pickle.dump(similarity_small, open(compressed_filename, 'wb'))
    
    file_size_mb = os.path.getsize(compressed_filename) / (1024 * 1024)
    print(f"Compressed file size: {file_size_mb:.2f} MB")

    # 4. Split the compressed file into 40MB chunks for GitHub
    # (GitHub limit is 100MB, but 40MB is safe and fast)
    chunk_size = 40 * 1024 * 1024 
    file_number = 1
    
    print("Splitting for GitHub...")
    with open(compressed_filename, 'rb') as f:
        chunk = f.read(chunk_size)
        while chunk:
            part_name = f"similarity.pkl.part{file_number}"
            with open(part_name, 'wb') as chunk_file:
                chunk_file.write(chunk)
            print(f"Created {part_name}")
            file_number += 1
            chunk = f.read(chunk_size)
    
    # Clean up the temporary single compressed file
    os.remove(compressed_filename)
    print("Done! You can now push the 'similarity.pkl.partX' files to GitHub.")

if __name__ == "__main__":
    compress_and_split()