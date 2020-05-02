#Importing libraries---
import pandas as pd
import numpy as np
import json
from bson import json_util
from django.shortcuts import render
from rest_framework.decorators import api_view,renderer_classes
from rest_framework.response import Response
from rest_framework import status
import pickle
import sys
import os
# from api.config import file_path
# path = file_path()
from django.conf import settings
MEDIA_FOLDER_PATH = settings.MEDIA_ROOT + '/'

@api_view(['GET'])
def getDescriptive(request):
	def descriptive_statistics(file):
		if os.path.exists(MEDIA_FOLDER_PATH + str(file)):
			df = pd.read_csv(MEDIA_FOLDER_PATH + str(file),na_values = ["NaN", 'NaT','','Missing','NA','na','N/A','n/a','nan','NAN'],encoding = "ISO-8859-1")
			df.replace(["NaN", 'NaT','','Missing','NA','na','N/A','n/a','nan','NAN'], np.nan, inplace = True)
			# Descriptive statistics for the numeric columns---
			df_num = round((df.describe()),3)
			response_num = json.loads(json_util.dumps(df_num))
			dict_num = json.dumps(response_num)
			my_dict_num = json.loads(dict_num)
			key_num = ['Numeric']
			val_num = [my_dict_num]
			keyval_num = dict(zip(key_num,val_num))
			# Finding categorical columns from the dataframe---
			cat_col = list(set(df.columns.tolist()) - set(df._get_numeric_data().columns.tolist()))
			# Descriptive statistics for the categorical columns---
			df_cat = df[cat_col].describe().to_dict()
			db = {}
			db['Category'] = df_cat
			# For storing---
			a = pickle.dumps(db)
			# For loading---
			keyval_cat = pickle.loads(a)
			# Adding 2 dictionaries---
			dict_final = {**keyval_num,**keyval_cat}
			return dict_final
		else:
			return {"errors":"failed to save the file"}

	if request.method == "GET":
		try:
			response = descriptive_statistics(request.GET.get('filename'))
			return Response(response)
		except Exception as e:
			print(e)
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(exc_type, fname, exc_tb.tb_lineno)
			return Response("Error in descriptive statistics response",status=status.HTTP_400_BAD_REQUEST)
	else:
		return Response("Error in GET response",status=status.HTTP_400_BAD_REQUEST)
