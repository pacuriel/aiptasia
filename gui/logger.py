import os
import logging
import sys



class Logger:
    """Class responsible for logging info relevant to application/user."""
    def __init__(self, log_dir="temp_log"):
        """Initializes logger class.
        
        Args:
            log_dir: String with directory path to save log files.
        """
        self.log_dir = log_dir # Directory to save log files
        self.__create_log_dir() # Creating log_directory

        self.__configure_logger() # Configuring logger

    def __configure_logger(self):
        logging.basicConfig(level=logging.INFO,
                            format='%(levelname)s, %(asctime)s, %(filename)s, %(funcName)s, %(message)s',
                            filename=f'{self.log_dir}/logfile.log',
                            filemode='a')
        
        console = logging.StreamHandler() # Handler to write to sys.stdout
        formatter = logging.Formatter('[%(levelname)s] %(message)s') # Format for console output
        console.setFormatter(fmt=formatter) # Assigning format to handler
        logging.getLogger(name=None).addHandler(console) # Adding handler to root logger

        sys.excepthook = self.__handle_uncaught_exception

    def __create_log_dir(self) -> None:
        """Creates log directory if it doesn't exist yet."""
        if not os.path.isdir(self.log_dir):
            os.makedirs(self.log_dir)

    def __handle_uncaught_exception(self, exc_type, exc_value, exc_traceback) -> None:
        """Handles uncaught exceptions and displays in logger."""
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return None

        logger = logging.getLogger(name=None)
        logger.error('Uncaught exception occured', exc_info=(exc_type, exc_value, exc_traceback))
