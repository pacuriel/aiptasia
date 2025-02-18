import os

class Logger:
    """Class responsible for logging info relevant to application/user."""
    def __init__(self, log_dir="temp_log"):
        """Initializes logger class.
        
        Args:
            log_dir: String with directory path to save log files.
        """
        self.log_dir = log_dir # Directory to save log files
        self.__create_log_dir() # Creating log_directory

    def __create_log_dir(self) -> None:
        """Creates log directory if it doesn't exist yet."""
        if not os.path.isdir(self.log_dir):
            os.makedirs(self.log_dir)