#Importing libraries---
import os
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
def getCorrelation(request):
	def corr_analysis_filter(w,x,y,z):
		if os.path.exists(MEDIA_FOLDER_PATH + str(w)):
			# Importing necessary csv file from the endpoint---
			df_corr = pd.read_csv(MEDIA_FOLDER_PATH + str(w),na_values = ["NaN", 'NaT','','Missing','NA','na','N/A','n/a','nan','NAN'],encoding = "ISO-8859-1")
			# Finding only the numeric columns---
			# numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64','double']
			# newdf = df_corr.select_dtypes(include=numerics)
			df_corr.replace(["NaN", 'NaT','','Missing','NA','na','N/A','n/a','nan','NAN'], np.nan, inplace = True)
			newdf1 = pd.DataFrame(df_corr[x])
			for columns in x:
				percentChar = '\%'
				if newdf1[columns].astype(str).str.contains(percentChar).any() :
					newdf1[columns]=newdf1[columns].replace(percentChar,'',regex=True).astype(float).div(100)
			# Imputing missing values---
			newdf1.fillna(0,inplace = True)
			# Subsetting the dataframe with selected columns---
			# Finding the correlation---
			result_corr = newdf1.corr()
			result_corr = round(result_corr,3)
			test={}
			for  i,j in result_corr.to_dict().items(): # Here j is another dictionary---
				temp={}
				for k,l in j.items():
					for m in range(len(y)) :
						if float(y[m]) < l <= float(z[m]) :
							temp[k] = l
						else:
							# temp[k]=0
							pass
							# test[i] = (k , 0)
				if temp:
					test[i] = temp
			# print(test)
			# response = json.loads(json_util.dumps(result_corr))
			# dict1 = json.dumps(response)
			# my_dict = json.loads(dict1)
			return test
		else:
			return {"errors":"failed to save the file"}


	def corr_analysis(x,y):
		if os.path.exists(MEDIA_FOLDER_PATH + str(x)):
			# Reading the csv file from the endpoint---
			df_corr = pd.read_csv(MEDIA_FOLDER_PATH + str(x),na_values = ['Missing','NA','na','N/A','n/a',''],encoding = "ISO-8859-1")
			# Selecting only numeric columns---
			# numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
			# newdf = df_corr.select_dtypes(include=numerics)
			df_corr.replace(["NaN", 'NaT','','Missing','NA','na','N/A','n/a','nan','NAN'], np.nan, inplace = True)
			# Imputing missing values---
			# Subsetting the dataframe with selected columns---
			newdf1 = pd.DataFrame(df_corr[y])
			newdf1.fillna(0,inplace = True)
			for columns in y:
				percentChar = '\%'
				if newdf1[columns].astype(str).str.contains(percentChar).any() :
					newdf1[columns]=newdf1[columns].replace(percentChar,'',regex=True).astype(float).div(100)
			# Finding correlation---
			result_corr = newdf1.corr()
			result_corr = round(result_corr,3)
			# Converting to dictionary from the dataframe---
			response = json.loads(json_util.dumps(result_corr))
			dict1 = json.dumps(response)
			my_dict = json.loads(dict1)
			return my_dict
		else:
			return {"errors":"failed to save the file"}


	if request.method == "POST":
		if request.data['method'] == 'filter' :
			try:
				responseCorr_filter = corr_analysis_filter(request.data['dataset'],request.data['columns'].split(','),
									request.data['range1'].split(','),request.data['range2'].split(','))
				return Response(responseCorr_filter)
			except Exception as e:
				print(e)
				exc_type, exc_obj, exc_tb = sys.exc_info()
				fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
				print(exc_type, fname, exc_tb.tb_lineno)
				return Response("Error in Correlation filter response",status=status.HTTP_400_BAD_REQUEST)
		elif request.data['method'] == 'all':
			try:
				responseCorr = corr_analysis(request.data['dataset'],request.data['columns'].split(','))
				return Response(responseCorr)
			except Exception as e:
				print(e)
				exc_type, exc_obj, exc_tb = sys.exc_info()
				fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
				print(exc_type, fname, exc_tb.tb_lineno)
				return Response("Error in Correlation response",status=status.HTTP_400_BAD_REQUEST)
	else:
		return Response("Error in POST response", status = status.HTTP_400_BAD_REQUEST)