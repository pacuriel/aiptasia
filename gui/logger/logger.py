import os
import logging
import sys
import configparser



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

        self.__check_csv()

        self.__setup_config_file() # Setup configuration file

    def __create_log_dir(self) -> None:
        """Creates log directory if it doesn't exist yet."""
        if not os.path.isdir(self.log_dir):
            os.makedirs(self.log_dir)

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
    
    def __check_csv(self):
        
        pass

    def __setup_config_file(self):
        ### Setting up configuration file
        self.config_name = "config.ini" # Name of configuration file
        self.config_path = os.path.join(self.log_dir, self.config_name)
        self.config = configparser.ConfigParser() # Create config parser
        if not os.path.isfile(self.config_path):
            ### Create config file here
            pass

    def __handle_uncaught_exception(self, exc_type, exc_value, exc_traceback) -> None:
        """Handles uncaught exceptions and displays in logger."""
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return None

        logger = logging.getLogger(name=None)
        logger.error('Uncaught exception occured', exc_info=(exc_type, exc_value, exc_traceback))

    def __check_section(self, section) -> None:
        """Check if a section exists in config file and create if not."""
        if not self.config.has_section(section):
            self.config.add_section(section)

    def save(self):
        """Saves config file."""
        # with open()

    