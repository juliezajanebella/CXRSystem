from datetime import datetime
import os


# def handle_uploaded_file(f):
#     # Get the current date as a string
#     date_str = datetime.now().strftime('(%m-%d-%Y)')  # This will be in the format 'MM-DD,YYYY'
    
#     # Split the filename and extension
#     filename, file_extension = os.path.splitext(f.name)
    
#     # Append the current date to the filename
#     new_filename = f"{filename}_{date_str}{file_extension}"
    
#     # Now save the file with the new filename
#     file_path = f'CXRaide/static/upload/raw_images/{new_filename}'
#     with open(file_path, 'wb+') as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)
