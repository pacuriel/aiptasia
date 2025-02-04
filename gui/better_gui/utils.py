"""Utility functions used throughout the application codebase."""

# Importing packages
from PIL import Image

def is_image(image_path) -> bool:
    """Determines if provided path is an image file.
    
    Args:
        image_path: path to a file to check

    Returns:
        A boolean that is true if provided path points to an image.
        Otherwise, returns false. 
    """

    is_image = True # Initializing boolean flag to true

    # Try-except block to open and close PIL image
    try:
        img = Image.open(image_path) # Opening PIL image 
        img.close() # Closing PIL image
    except: 
        is_image = False # Updating boolean flag if not image

    return is_image # Returning boolean flag