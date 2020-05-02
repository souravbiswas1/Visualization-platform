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
# from api.config import file_path
# path = file_path()
from django.conf import settings
MEDIA_FOLDER_PATH = settings.MEDIA_ROOT + '/'


@api_view(['GET'])
def getUnivar(request):
	def univar_analysis_num(x,y,z):
		if os.path.exists(MEDIA_FOLDER_PATH + str(z)):
			# Reading csv from the endpoint---
			df_univar = pd.read_csv(MEDIA_FOLDER_PATH + str(z),na_values = ['Missing','NA','na','N/A','n/a',''],encoding = "ISO-8859-1")
			#Finding only the numeric columns---
			# df_univar_num = df_univar._get_numeric_data()
			# Converting all missing values into numpy object---
			df_univar.replace(["NaN", 'NaT','','Missing','NA','na','N/A','n/a','nan','NAN'], np.nan, inplace = True)
			df_univar_num = pd.DataFrame(df_univar[x])
			df_univar_num[x] = round(df_univar_num[x],4)
			df_univar_num.fillna(0,inplace = True)
			percentChar = '\%'
			if df_univar_num[x].astype(str).str.contains(percentChar).any() :
				df_univar_num[x]=df_univar_num[x].replace(percentChar,'',regex=True).astype(float).div(100)

			s1 = ((df_univar_num[x] // float(y)) * float(y)).min()
			s2 = ((df_univar_num[x] // float(y) + 1) * float(y)).max()
			bins = np.arange(s1, s2 + float(y), float(y))
			labels = [f'{float(i)}-{float(j)}' for i, j in zip(bins[:-1], bins[1:])] 
			df_univar_num['bin'] = pd.cut(df_univar_num[x], bins = bins, labels = labels, right = False)

			df_bin = df_univar_num.groupby(['bin']).size().reset_index(name='counts')
			df_bin['bin_percentage'] = pd.DataFrame(round(df_bin['counts'] / sum(df_bin['counts']) * 100))

			response = json.loads(json_util.dumps(df_univar_num))
			dict1 = json.dumps(response)
			my_dict = json.loads(dict1)

			response_bin = json.loads(json_util.dumps(df_bin))
			dict_bin = json.dumps(response_bin)
			my_dict_bin = json.loads(dict_bin)

			key1 = [x]
			val1 = [my_dict]
			keyval1 = dict(zip(key1,val1))

			key2 = [str(x) + '_bin']
			val2 = [my_dict_bin]
			keyval2 = dict(zip(key2,val2))

			dict_final = {**keyval1,**keyval2}
			return dict_final
		else:
			return {"errors":"failed to save the file"}


	def univar_analysis_cat(y,z):
		if os.path.exists(MEDIA_FOLDER_PATH + str(z)):
			# Reading csv from the endpoint---
			df_univar = pd.read_csv(MEDIA_FOLDER_PATH + str(z),na_values = ['Missing','NA','na','N/A','n/a',''],encoding = "ISO-8859-1")
		# 	#Finding only categorical columns---
			df_univar_cat = df_univar.select_dtypes(exclude=["number"])
			# Converting all the missing values into numpy object---
			df_univar_cat.replace(["NaN", 'NaT','','Missing','NA','na','N/A','n/a','nan','NAN'], np.nan, inplace = True)
			# Dropping the rows containing missing values---
			df_univar_cat = df_univar_cat.fillna('Data not available')


			# Subsetting dataframe with selected column---
			df_out = df_univar_cat[[y]]
			# Finding frequency count for the category---
			df_out = pd.DataFrame(df_out[y].value_counts())
			# Creating dictionary from the dataframe---
			response = json.loads(json_util.dumps(df_out))
			dict1 = json.dumps(response)
			my_dict1 = json.loads(dict1)
			# Finding the percentage of the category---
			perc1 = pd.DataFrame(round(df_out[y] / sum(df_out[y]) * 100))
			perc1 = perc1.rename(columns={ y : str(y) + '_Percentage'})
			response1 = json.loads(json_util.dumps(perc1))
			dict2 = json.dumps(response1)
			my_dict2 = json.loads(dict2)
			my_dict = {**my_dict1,**my_dict2}
			return my_dict
		else:
			return {"errors":"failed to save the file"}


	if request.method =="GET":
		if request.GET.get('method') == 'numeric univariate' :
			try:
				respUnivarNum = univar_analysis_num(request.GET.get('univar_num'),request.GET.get('bin_range'),request.GET.get('dataset'))
				return Response(respUnivarNum)
			except Exception as e:
				print(e)
				return Response("Error in Numeric Univariate for insufficient data",status=status.HTTP_400_BAD_REQUEST)
		elif request.GET.get('method') == 'categorical univariate' :
			try:
				respUnivarCat = univar_analysis_cat(request.GET.get('univar_cat'),request.GET.get('dataset'))
				return Response(respUnivarCat)
			except Exception as e:
				print(e)
				return Response("Error in Categorical Univariate for insufficient data",status=status.HTTP_400_BAD_REQUEST)
	else:
		return Response("Error in GET request",status=status.HTTP_400_BAD_REQUEST)
