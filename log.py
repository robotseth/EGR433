import numpy as np
import glob
import os
from loguru import logger

class Log:
    def __init__(self, data = np.ones(4), name='logged_data', folder='data', titles = ['Alpha','Theta','Response','Time']):
        self.name = name
        self.folder = folder
        self.data = data
        self.titles = titles

    def append_internal(self, new_data):
        try:
            self.data = np.vstack((self.data,new_data))
        except Exception as e:
            logger.error(e)

    def save_log_internal(self, data, titles, name, folder):
        # remove the first row of empty values
        self.data = np.delete(self.data, 0, 0)

        # create the full file path
        cwd = os.getcwd()
        data_folder = folder

        # define the base file name and extension
        base_name = name
        ext = '.csv'

        # find all files with the same base name and extension
        files = glob.glob(f'{cwd}/{data_folder}/{base_name}_*{ext}')

        # sort the files by name
        files.sort()

        # get the number from the last file name
        if files:
            last_file = os.path.splitext(files[-1])[0]
            last_num = int(last_file.split('_')[-1])
        else:
            last_num = 0

        # create the new file name with an incremented number
        new_file = f'{base_name}_{last_num+1}{ext}'
        new_file_path = os.path.join(cwd, data_folder, new_file)
        # combine the column titles and data into a single array
        data_with_titles = np.vstack((titles, data))
        # save the data to a CSV file with headers
        np.savetxt(new_file_path, data_with_titles, delimiter=',', header='', comments='', fmt='%s')
        logger.success(f'Data saved as {new_file} in {folder}')

    def log(self, data):
        try:
            # convert the data to a numpy array if possible
            if not isinstance(data, np.ndarray):
                data = np.array(data)
            # calls the function that appends data to the main array
            self.append_internal(data)
        except Exception as e:
            logger.error(e)
    
    def save(self):
        try:
            self.save_log_internal(data=self.data, titles=self.titles, name=self.name, folder=self.folder)
        except Exception as e:
            logger.error(e)

