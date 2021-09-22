from django.core.files.storage import FileSystemStorage
import os
import pandas as pd
from django.conf import settings
MEDIA_FOLDER_PATH = settings.MEDIA_ROOT + '\\'


def read_data(filename):
    file_url = MEDIA_FOLDER_PATH + filename
    if os.path.exists(file_url):
        df = pd.read_csv(file_url,
                         na_values=["NaN", 'NaT', '', 'Missing', 'NA', 'na', 'N/A', 'n/a', 'nan', 'NAN'],
                         encoding="ISO-8859-1")
        return df
    else:
        return {"errors": "failed to save the file"}

