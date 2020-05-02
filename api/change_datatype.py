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

@api_view(['POST'])
def getNumToCat(request):
	def data_type(file,col):
		if os.path.exists(MEDIA_FOLDER_PATH + str(file)):
			df = pd.read_csv(MEDIA_FOLDER_PATH + str(file),na_values = ["NaN", 'NaT','','Missing','NA','na','N/A','n/a','nan','NAN'],encoding = "ISO-8859-1")
			df.replace(["NaN", 'NaT','','Missing','NA','na','N/A','n/a','nan','NAN'], np.nan, inplace = True)

			# df[col] = df.to_string(columns = [col])
			df[col] = df[col].astype(str)
			df_num = df._get_numeric_data()

			cat_col = set(df.columns.tolist()) - set(df_num.columns.tolist())
			cat_list = list(cat_col)

			num_list = list(df_num.columns.tolist())
			key1 = ['Numeric columns']
			val1 = [num_list]
			keyval1 = dict(zip(key1,val1))

			key2 = ['Categorical columns']
			val2 = [cat_list]
			keyval2 = dict(zip(key2,val2))

			keyval = {**keyval1,**keyval2}
			return keyval
		else:
			return {"errors":"failed to save the file"}

	if request.method == "POST":
		try:
			response = data_type(request.data['dataset'],request.data['columns'].split(','))
			return Response(response)
		except Exception as e:
			print(e)
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(exc_type, fname, exc_tb.tb_lineno)
			return Response("Error in column data type response",status=status.HTTP_400_BAD_REQUEST)
	else:
		return Response("Error in POST response",status=status.HTTP_400_BAD_REQUEST)
