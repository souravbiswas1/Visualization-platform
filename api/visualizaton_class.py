import pandas as pd
import logging
import os
from django.conf import settings
MEDIA_FOLDER_PATH = settings.MEDIA_ROOT + '\\'

class Visualization:
  def __init__(self):
    logging.info(f"initialization of Visualization class")
    # self.filename = filename # Name of the file to be uploaded
    # self.path = path         # path of file within the server

  def read_data(self, file_name):
    file_url = MEDIA_FOLDER_PATH + file_name
    if os.path.exists(file_url):
      df = pd.read_csv(file_url, na_values=["NaN", 'NaT', '', 'Missing', 'NA', 'na', 'N/A', 'n/a', 'nan', 'NAN'],encoding="ISO-8859-1")
      return df
    else:
      return {"errors": "failed to save the file"}

