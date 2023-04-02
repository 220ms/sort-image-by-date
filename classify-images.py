import os
import exifread
from datetime import datetime
import shutil

# Define the input and output directories
input_dir = r"input path here"
output_dir = r"output path here" 

# Define a function to extract the date from the image metadata
def get_date_taken(file_path):
    with open(file_path, 'rb') as f:
        tags = exifread.process_file(f)
        if 'EXIF DateTimeOriginal' in tags:
            date_str = str(tags['EXIF DateTimeOriginal'])
            date_obj = datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S')
            return date_obj.strftime('%Y-%m-%d')
        else:
            return None

# Create a dictionary to store the date-based directories
date_dirs = {}

# Loop through all .NEF files in the input directory
count = 0
length = len(os.listdir(input_dir))
for filename in os.listdir(input_dir):  
    count += 1 
     
    # Get the full path to the file
    file_path = os.path.join(input_dir, filename)
    
    # Get the date taken from the image metadata
    date_taken = get_date_taken(file_path)
    
    # If the date taken is valid, copy the file to the corresponding date-based directory
    if date_taken:
        if date_taken not in date_dirs:
            # Create a new directory for the date if it doesn't exist
            date_dir = os.path.join(output_dir, date_taken)
            os.makedirs(date_dir, exist_ok=True)
            date_dirs[date_taken] = date_dir
        # Copy the file to the date-based directory
        dest_path = os.path.join(date_dirs[date_taken], filename)
        shutil.copy2(file_path, dest_path)