import os
import sys
from exception import CustomException

def save_file(file_path, obj):
    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, 'wb') as file_obj:
            file_obj.write(obj)
    except Exception as e:
        raise CustomException(e, sys)