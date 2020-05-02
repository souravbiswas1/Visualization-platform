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
import pandas.core.algorithms as algos
# from api.config import file_path
# path = file_path()
from django.conf import settings
MEDIA_FOLDER_PATH = settings.MEDIA_ROOT + '/'


@api_view(['POST'])
def getMultivar(request):
	def multivar_num_mean(x,y,z):
		if os.path.exists(MEDIA_FOLDER_PATH + str(x)):
			df_bivar = pd.read_csv(MEDIA_FOLDER_PATH + str(x),na_values = ['Missing','NA','na','N/A','n/a',''],encoding = "ISO-8859-1")
			# Converting all missing values into numpy object---
			df_bivar.replace(["NaN", 'NaT','','Missing','NA','na','N/A','n/a','nan','NAN'], np.nan, inplace = True)
			# percentChar = '\%'
			# # if df_bivar_num[x].astype(str).str.contains(percentChar).any() :
			# # 	df_bivar_num[x] = df_bivar_num[x].replace(percentChar,'',regex=True).astype(float).div(100)
			# if df_bivar_num[y].astype(str).str.contains(percentChar).any() :
			# 	df_bivar_num[y]=df_bivar_num[y].replace(percentChar,'',regex=True).astype(float).div(100)
			df_bivar.fillna(0,inplace = True)	
			# df_out = df_bivar_num[y]
			final_df = df_bivar.groupby([z])[y].mean()
			# Creating dictionary from the dataframe---
			response = json.loads(json_util.dumps(final_df))
			dict1 = json.dumps(response)
			my_dict = json.loads(dict1)
			return my_dict
		else:
			return {"errors":"failed to save the file"}


	def multivar_num_sum(x,y,z):
		if os.path.exists(MEDIA_FOLDER_PATH + str(x)):
			df_bivar = pd.read_csv(MEDIA_FOLDER_PATH + str(x),na_values = ['Missing','NA','na','N/A','n/a',''],encoding = "ISO-8859-1")
			# Converting all missing values into numpy object---
			df_bivar.replace(["NaN", 'NaT','','Missing','NA','na','N/A','n/a','nan','NAN'], np.nan, inplace = True)
			# percentChar = '\%'
			# # if df_bivar_num[x].astype(str).str.contains(percentChar).any() :
			# # 	df_bivar_num[x] = df_bivar_num[x].replace(percentChar,'',regex=True).astype(float).div(100)
			# if df_bivar_num[y].astype(str).str.contains(percentChar).any() :
			# 	df_bivar_num[y]=df_bivar_num[y].replace(percentChar,'',regex=True).astype(float).div(100)
			df_bivar.fillna(0,inplace = True)	
			# df_out = df_bivar_num[y]
			final_df = df_bivar.groupby([z])[y].sum()
			# Creating dictionary from the dataframe---
			response = json.loads(json_util.dumps(final_df))
			dict1 = json.dumps(response)
			my_dict = json.loads(dict1)
			return my_dict
		else:
			return {"errors":"failed to save the file"}


	def multivar_cat(w,x,y):
		if os.path.exists(MEDIA_FOLDER_PATH + str(w)):
			# Importing necessary csv file from the endpoint---
			df = pd.read_csv(MEDIA_FOLDER_PATH + str(w),na_values = ["NaN", 'NaT','','Missing','NA','na','N/A','n/a','nan','NAN'],encoding = "ISO-8859-1")
			df.replace(["NaN", 'NaT','','Missing','NA','na','N/A','n/a','nan','NAN'], np.nan, inplace = True)
			df.fillna('Missing/NA')
			# df_out = df[x]
			final_df = df.groupby(x)[y].count().reset_index()
			# final_df1 = final_df.rename(columns = {str(x) : 'Counts_Val'})
			# print(final_df1)
			response = json.loads(json_util.dumps(final_df))
			# temp = {}
			# for i in x:
			# 	temp.update({i:(df[i].value_counts())})
			# response = json.loads(json_util.dumps(temp).replace("\'", ''))
			dict1 = json.dumps(response)
			my_dict = json.loads(dict1)
			return my_dict
		else:
			return {"errors":"failed to save the file"}


	def multivar_num(y,z):
		if os.path.exists(MEDIA_FOLDER_PATH + str(y)):
			# Reading the csv file from the endpoint---
			df_bivar = pd.read_csv(MEDIA_FOLDER_PATH + str(y),na_values = ['Missing','NA','na','N/A','n/a',''],encoding = "ISO-8859-1")
			# Converting all missing values into numpy object---
			df_bivar.replace(["NaN", 'NaT','','Missing','NA','na','N/A','n/a','nan','NAN'], np.nan, inplace = True)
			df_bivar_num = pd.DataFrame(df_bivar[z])
			# percentChar = '\%'
			# if df_bivar_num[y].astype(str).str.contains(percentChar).any() :
			# 	df_bivar_num[y]=df_bivar_num[y].replace(percentChar,'',regex=True).astype(float).div(100)
			df_bivar_num.fillna(0,inplace = True)
			df_bivar_num = round(df_bivar_num,4)
			# df_out = df_bivar_num[[x,y]]
			# Creating dictionary from the dataframe---
			response = json.loads(json_util.dumps(df_bivar_num))
			dict1 = json.dumps(response)
			my_dict = json.loads(dict1)
			return my_dict
		else:
			return {"errors":"failed to save the file"}


	def frequency_dist_num(x,y,z):
		if os.path.exists(MEDIA_FOLDER_PATH + str(x)):
			df_Frequency = pd.read_csv(MEDIA_FOLDER_PATH + str(x),na_values = ['Missing','NA','na','N/A','n/a',''],encoding = "ISO-8859-1")
			df_Frequency.replace(["NaN", 'NaT','','Missing','NA','na','N/A','n/a','nan','NAN'], np.nan, inplace = True)
			for columns in y:
				percentChar = '\%'
				if df_Frequency[columns].astype(str).str.contains(percentChar).any() :
					df_Frequency[columns]=df_Frequency[columns].replace(percentChar,'',regex=True).astype(float).div(100)
			# df_Frequency_Cat = df_Frequency.select_dtypes(exclude = ["number"])
			# df_Frequency_Cat = df_Frequency_Cat.fillna('Missing/NA')
			df_Frequency_Num = df_Frequency._get_numeric_data()
			df_Frequency_Num = df_Frequency_Num.fillna(0)
			df_Frequency_Num.reset_index(inplace=True)
			temp={}
			for i in y:
				df = pd.cut(df_Frequency_Num[i],int(z),right=False,include_lowest=False).value_counts()
				df.index = df.index.astype(str)
				dict_n = df.to_dict()
				temp.update({i:dict_n})
			# for j in z:
			# 	temp.update({j:(df_Frequency_Cat[j].value_counts())})

			response = json.loads(json_util.dumps(temp).replace("\'", ''))
			dict1 = json.dumps(response)
			my_dict = json.loads(dict1)
			return my_dict
		else:
			return {"errors":"failed to save the file"}


	def frequency_dist_cat(x,y):
		if os.path.exists(MEDIA_FOLDER_PATH + str(x)):
			df_Frequency = pd.read_csv(MEDIA_FOLDER_PATH + str(x),na_values = ['Missing','NA','na','N/A','n/a',''],encoding = "ISO-8859-1")
			df_Frequency.replace(["NaN", 'NaT','','Missing','NA','na','N/A','n/a','nan','NAN'], np.nan, inplace = True)
			for columns in y:
				percentChar = '\%'
				if df_Frequency[columns].astype(str).str.contains(percentChar).any() :
					df_Frequency[columns]=df_Frequency[columns].replace(percentChar,'',regex=True).astype(float).div(100)
			df_Frequency_Cat = df_Frequency.select_dtypes(exclude = ["number"])
			df_Frequency_Cat = df_Frequency_Cat.fillna('Missing/NA')
			# df_Frequency_Num = df_Frequency._get_numeric_data()
			# df_Frequency_Num = df_Frequency_Num.fillna(0)
			# df_Frequency_Num.reset_index(inplace=True)
			temp={}
			# for i in y:
			# 	df = pd.cut(df_Frequency_Num[i],10,right=False).value_counts()
			# 	df.index = df.index.astype(str)
			# 	dict_n = df.to_dict()
			# 	temp.update({i:dict_n})
			for j in y:
				temp.update({j:(df_Frequency_Cat[j].value_counts())})

			response = json.loads(json_util.dumps(temp).replace("\'", ''))
			dict1 = json.dumps(response)
			my_dict = json.loads(dict1)
			return my_dict
		else:
			return {"errors":"failed to save the file"}


	if request.method == "POST":
		if request.data['method'] == 'numeric multivariate mean' :
			try:
				respNum_mean = multivar_num_mean(request.data['dataset'],request.data['columns'].split(','),request.data['groupby'])
				return Response(respNum_mean)
			except Exception as e:
				print(e)
				return Response("Error in numeric multivariate",status=status.HTTP_400_BAD_REQUEST)
		elif request.data['method'] == 'numeric multivariate sum' :
			try:
				respNum_sum = multivar_num_sum(request.data['dataset'],request.data['columns'].split(','),request.data['groupby'])
				return Response(respNum_sum)
			except Exception as e:
				print(e)
				return Response("Error in numeric multivariate",status=status.HTTP_400_BAD_REQUEST)
		elif request.data['method'] == 'categorical multivariate' :
			try:
				respCat = multivar_cat(request.data['dataset'],request.data['columns'].split(','),request.data['groupby'])
				return Response(respCat)
			except Exception as e:
				print(e)
				return Response("Error in categorical multivariate",status=status.HTTP_400_BAD_REQUEST)
		elif request.data['method'] == 'numerical multivariate' :
			try:
				respNum = multivar_num(request.data['dataset'],request.data['columns'].split(','))
				return Response(respNum)
			except Exception as e:
				print(e)
				return Response("Error in categorical multivariate",status=status.HTTP_400_BAD_REQUEST)
		elif request.data['method'] == 'num all multivariate' :
			try:
				respAllNum = frequency_dist_num(request.data['dataset'],request.data['numcol'].split(','),request.data['histogram_bin'])
				return Response(respAllNum)
			except Exception as e:
				print(e)
				return Response("Error in all numeric multivariate",status=status.HTTP_400_BAD_REQUEST)
		elif request.data['method'] == 'cat all multivariate' :
			try:
				respAllCat = frequency_dist_cat(request.data['dataset'],request.data['catcol'].split(','))
				return Response(respAllCat)
			except Exception as e:
				print(e)
				return Response("Error in all categorical multivariate",status=status.HTTP_400_BAD_REQUEST)
	else:
		return Response("Error in POST request",status=status.HTTP_400_BAD_REQUEST)