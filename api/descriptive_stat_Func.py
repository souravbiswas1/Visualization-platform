#Importing libraries---
# import pandas as pd
# import numpy as np
import json
from bson import json_util
# from django.shortcuts import render
from rest_framework.decorators import api_view,renderer_classes
from rest_framework.response import Response
from rest_framework import status
import pickle
import sys
import os
from django.conf import settings
MEDIA_FOLDER_PATH = settings.MEDIA_ROOT + '/'
from .utils import read_data

@api_view(['GET'])
def getDescriptive(request):
	def descriptive_statistics(filename):
		df = read_data(filename)
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
		store = pickle.dumps(db)
		if (store):
			# For loading---
			keyval_cat = pickle.loads(store)
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
