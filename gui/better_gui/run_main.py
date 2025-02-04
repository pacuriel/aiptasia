"""Code obtained and adapted from: https://github.com/foobar167/junkyard/tree/master/manual_image_annotation1."""
from main_window import MainWindow

def main(): 
    """Main function"""
    main_window = MainWindow() # Storing MainWindow object
    main_window.mainloop() # Running application

    ### Use logger? 

if __name__ == "__main__":
    main()