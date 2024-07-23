import logging
import os
from datetime import datetime

'''
Run it as: logging.info('your message')
Messages will be logged in the format below
'''
logging_options={0:logging.CRITICAL, 1:logging.INFO}

# Turn logging ON(1) or OFF(0)
LOG_OR_NOT= 1

if LOG_OR_NOT:

    LOG_FILE_NAME=f"{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}.log"

    logs_path= os.path.join(os.getcwd(),'logs')
    os.makedirs(logs_path,exist_ok=True)

    LOG_FILE_PATH= os.path.join(logs_path,LOG_FILE_NAME)

    logging.basicConfig(
        filename=LOG_FILE_PATH,
        format='[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s',
        level=logging_options[LOG_OR_NOT]
    )

else:
    pass