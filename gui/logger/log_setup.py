import os
import sys
import logging

def init_logging():
    log_dir = "temp_log"
    __create_log_dir(log_dir)
    __configure_logger(log_dir)
    __create_prompting_csv(log_dir)

def __create_log_dir(log_dir):
    """Creates log directory if it doesn't exist yet."""
    if not os.path.isdir(log_dir):
        os.makedirs(log_dir)

def __configure_logger(log_dir):
    logging.basicConfig(level=logging.INFO,
                        format='%(levelname)s, %(asctime)s, %(filename)s, %(funcName)s, %(message)s',
                        filename=f'{log_dir}/logfile.log',
                        filemode='a')
    
    console = logging.StreamHandler() # Handler to write to sys.stdout
    formatter = logging.Formatter('[%(levelname)s] %(message)s') # Format for console output
    console.setFormatter(fmt=formatter) # Assigning format to handler
    logging.getLogger(name=None).addHandler(console) # Adding handler to root logger

    sys.excepthook = __handle_uncaught_exception

def __create_prompting_csv(log_dir):
    prompt_csv_path = os.path.join(log_dir, "prompting.csv")

    # Checking if file exists and creating if not
    if not os.path.exists(prompt_csv_path):
        with open(prompt_csv_path, 'w') as csv:
            csv.write("file_name,prompt_id,point_x,point_y,is_pos,aip_id,canvas_oval_id\n")

### Helper function
def __handle_uncaught_exception(self, exc_type, exc_value, exc_traceback) -> None:
    """Handles uncaught exceptions and displays in logger."""
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return None

    logger = logging.getLogger(name=None)
    logger.error('Uncaught exception occured', exc_info=(exc_type, exc_value, exc_traceback))
