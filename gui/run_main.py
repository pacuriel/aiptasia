"""Code obtained and adapted from: https://github.com/foobar167/junkyard/tree/master/manual_image_annotation1."""
import logging

from main_window import MainWindow
from logger import Logger

def main(): 
    """Main function"""
    # Initalizing logger
    logger = Logger()
    logging.info("Starting application") # Startup message

    main_window = MainWindow() # Storing MainWindow object
    main_window.mainloop() # Running application
    logging.info("Exiting application") # Exit message

if __name__ == "__main__":
    main()