import os
import glob
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

def resize_image(input_image_path, output_image_path, max_width, max_height, output_format=None, quality=85):
    original_size = os.path.getsize(input_image_path)
    with Image.open(input_image_path) as img:
        original_width, original_height = img.size
        print(f"Processing {input_image_path} - Original size: {original_width}x{original_height}")
        
        aspect_ratio = original_width / original_height
        if original_width > original_height:
            new_width = min(max_width, original_width)
            new_height = int(new_width / aspect_ratio)
        else:
            new_height = min(max_height, original_height)
            new_width = int(new_height * aspect_ratio)
        
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        print(f"Resized to: {new_width}x{new_height}")
        
        if output_format is None:
            if img.format:
                output_format = img.format
            else:
                output_format = os.path.splitext(input_image_path)[1][1:]
        
        if output_format.upper() == 'JPG':
            output_format = 'JPEG'
        
        img.save(output_image_path, format=output_format.upper(), optimize=True, quality=quality)
        print(f"Saved image to {output_image_path} with format {output_format.upper()} and quality {quality}")
    
    new_size = os.path.getsize(output_image_path)
    print(f"Original file size: {original_size / 1024:.2f} KB")
    print(f"New file size: {new_size / 1024:.2f} KB\n")

def process_folder(input_folder, output_folder, max_width, max_height, output_format=None, quality=85):
    print(f"Current working directory: {os.getcwd()}")
    
    input_folder = os.path.abspath(input_folder)
    output_folder = os.path.abspath(output_folder)
    
    print(f"Input folder: {input_folder}")
    print(f"Output folder: {output_folder}")

    if not os.path.exists(input_folder):
        print(f"Error: Input folder '{input_folder}' does not exist.")
        return

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Output folder created: {output_folder}")

    all_files = os.listdir(input_folder)
    print(f"All files in input folder: {all_files}")
    
    image_formats = ('*.jpg', '*.jpeg', '*.png', '*.webp')
    
    print(f"Image formats to look for: {image_formats}")
    
    image_files = []
    
    for format in image_formats:
        search_pattern = os.path.join(input_folder, format)
        print(f"Searching for: {search_pattern}")
        image_files.extend(glob.glob(search_pattern))
    
    if not image_files:
        print("No image files found in the specified folder.")
        return

    print(f"Found {len(image_files)} image(s) to process: {image_files}")
    
    for image_file in image_files:
        file_name, original_extension = os.path.splitext(os.path.basename(image_file))

        if output_format is None:
            output_extension = original_extension
        else:
            output_extension = f".{output_format.lower()}"

        output_image_path = os.path.join(output_folder, f"{file_name}{output_extension}")
        resize_image(image_file, output_image_path, max_width, max_height, output_format, quality)

input_folder = "."
output_folder = "."
output_format = None
process_folder(input_folder, output_folder, max_width=800, max_height=600, output_format=output_format)
