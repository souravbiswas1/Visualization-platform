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
def getBivar(request):
	def bivar_analysis_cat(x,y,z):
		if os.path.exists(MEDIA_FOLDER_PATH + str(z)):
			# Reading the csv file from the endpoint---
			df_bivar = pd.read_csv(MEDIA_FOLDER_PATH + str(z),na_values = ['Missing','NA','na','N/A','n/a',''],encoding = "ISO-8859-1")
			# Retrieving only the categorical column---
			df_bivar_cat = df_bivar.select_dtypes(exclude = ["number"])
			# Converting the missing values into numpy object---
			df_bivar_cat.replace(["NaN", 'NaT','','Missing','NA','na','N/A','n/a','nan','NAN'], np.nan, inplace = True)
			# Dropping the rows containg missing values---
			df_bivar_cat = df_bivar_cat.fillna('Data not available')
			df_out = df_bivar_cat[[x,y]]
			# Getting the frequency count of the category---
			df_out1 = pd.DataFrame(df_out[x].value_counts())
			df_out1 = df_out1.rename(columns={'index' : 'Category_name1'})
			df_out2 = pd.DataFrame(df_out[y].value_counts())
			df_out2 = df_out2.rename(columns={'index' : 'Category_name2'})
			# Creating dictionary from the dataframe---	
			response1 = json.loads(json_util.dumps(df_out1))
			dict1 = json.dumps(response1)
			my_dict1 = json.loads(dict1)
			# Creating dictionary from the dataframe---
			response2 = json.loads(json_util.dumps(df_out2))
			dict2 = json.dumps(response2)
			my_dict2 = json.loads(dict2)
			# Finding the percentage of the category---
			perc1 = pd.DataFrame(df_out1[x] / sum(df_out1[x]) * 100)
			perc1 = round(perc1,3)
			perc1 = perc1.rename(columns={ x : str(x) + '_Percentage'})
			response3 = json.loads(json_util.dumps(perc1))
			dict3 = json.dumps(response3)
			my_dict3 = json.loads(dict3)
			# Finding the percentage of the category---
			perc2 = pd.DataFrame(df_out2[y] / sum(df_out2[y]) * 100)
			perc2 = round(perc2,3)
			perc2 = perc2.rename(columns={ y : str(y) + '_Percentage'})
			response4 = json.loads(json_util.dumps(perc2))
			dict4 = json.dumps(response4)
			my_dict4 = json.loads(dict4)
			# Concatenating all the dictionary---
			my_dict5 = {**my_dict1,**my_dict2}
			my_dict6 = {**my_dict3,**my_dict4}
			my_dict7 = {**my_dict5,**my_dict6}
			return my_dict7
		else:
			return {"errors":"failed to save the file"}

	def bivar_analysis_num(x,y,z):
		if os.path.exists(MEDIA_FOLDER_PATH + str(z)):
			# Reading the csv file from the endpoint---
			df_bivar = pd.read_csv(MEDIA_FOLDER_PATH + str(z),na_values = ['Missing','NA','na','N/A','n/a',''],encoding = "ISO-8859-1")
			#Finding only the numeric columns---
			# df_univar_num = df_univar._get_numeric_data()
			# Converting all missing values into numpy object---
			df_bivar.replace(["NaN", 'NaT','','Missing','NA','na','N/A','n/a','nan','NAN'], np.nan, inplace = True)
			df_bivar_num = pd.DataFrame(df_bivar[[x,y]])
			df_bivar_num[[x,y]] = round(df_bivar_num[[x,y]],4)
			percentChar = '\%'
			if df_bivar_num[x].astype(str).str.contains(percentChar).any() :
				df_bivar_num[x] = df_bivar_num[x].replace(percentChar,'',regex=True).astype(float).div(100)
			if df_bivar_num[y].astype(str).str.contains(percentChar).any() :
				df_bivar_num[y]=df_bivar_num[y].replace(percentChar,'',regex=True).astype(float).div(100)

			df_bivar_num.fillna(0,inplace = True)	
			df_out = df_bivar_num[[x,y]]
			# Creating dictionary from the dataframe---
			response = json.loads(json_util.dumps(df_out))
			dict1 = json.dumps(response)
			my_dict = json.loads(dict1)
			return my_dict
		else:
			return {"errors":"failed to save the file"}

	def bivar_sum(x,y,z):
		if os.path.exists(MEDIA_FOLDER_PATH + str(z)):
			# Reading the csv from the endpoint---
			df_bivar = pd.read_csv(MEDIA_FOLDER_PATH + str(z),na_values = ['Missing','NA','na','N/A','n/a',''],encoding = "ISO-8859-1")
			# Converting the missing values into numpy object---
			df_bivar.replace(["NaN", 'NaT','','Missing','NA','na','N/A','n/a','nan','NAN'], np.nan, inplace = True)
			df_bivar_num = pd.DataFrame(df_bivar[y])
			# percentChar = '\%'
			# if df_bivar_num[y].astype(str).str.contains(percentChar).any() :
			df_bivar_num[y] = df_bivar_num[y].replace('\%','',regex=True).astype(float)
			df_bivar_num.fillna(0,inplace = True)
			# Excluding the numeric columns---
			df_bivar_cat = df_bivar.select_dtypes(exclude = ["number"])
			df_bivar_cat = df_bivar_cat.fillna('Missing/NA')
			df_bivar_cat = pd.DataFrame(df_bivar_cat[x])

			df_out = pd.concat([df_bivar_cat, df_bivar_num], axis=1, sort=False)
			df_out_sum = df_out.groupby([x])[y].sum().reset_index()
			df_out_sum = round(df_out_sum,5)
			# Creating dictionary from the dataframe---
			response = json.loads(json_util.dumps(df_out_sum))
			dict1 = json.dumps(response)
			my_dict = json.loads(dict1)
			return my_dict
		else:
			return {"errors":"failed to save the file"}

	def bivar_mean(x,y,z):
		if os.path.exists(MEDIA_FOLDER_PATH + str(z)):
			# Reading the csv from the endpoint---
			df_bivar = pd.read_csv(MEDIA_FOLDER_PATH + str(z),na_values = ['Missing','NA','na','N/A','n/a',''],encoding = "ISO-8859-1")
			# Converting the missing values into numpy object---
			df_bivar.replace(["NaN", 'NaT','','Missing','NA','na','N/A','n/a','nan','NAN'], np.nan, inplace = True)
			df_bivar_num = pd.DataFrame(df_bivar[y])
			# percentChar = '\%'
			# if df_bivar_num[y].astype(str).str.contains(percentChar).any() :
			df_bivar_num[y] = df_bivar_num[y].replace('\%','',regex=True).astype(float)
			df_bivar_num.fillna(0,inplace = True)
			# Excluding the numeric columns---
			df_bivar_cat = df_bivar.select_dtypes(exclude = ["number"])
			df_bivar_cat = df_bivar_cat.fillna('Missing/NA')
			df_bivar_cat = pd.DataFrame(df_bivar_cat[x])

			df_out = pd.concat([df_bivar_cat, df_bivar_num], axis=1, sort=False)
			df_out_mean = df_out.groupby([x])[y].mean().reset_index()
			df_out_mean = round(df_out_mean,5)
			# Creating dictionary from the dataframe---
			response = json.loads(json_util.dumps(df_out_mean))
			dict1 = json.dumps(response)
			my_dict = json.loads(dict1)
			return my_dict
		else:
			return {"errors":"failed to save the file"}


	def bivar_sum_mean(x,y,z):
		if os.path.exists(MEDIA_FOLDER_PATH + str(z)):
			# Reading the csv from the endpoint---
			df_bivar = pd.read_csv(MEDIA_FOLDER_PATH + str(z),na_values = ['Missing','NA','na','N/A','n/a',''],encoding = "ISO-8859-1")
			# Converting the missing values into numpy object---
			df_bivar.replace(["NaN", 'NaT','','Missing','NA','na','N/A','n/a','nan','NAN'], np.nan, inplace = True)
			df_bivar_num = pd.DataFrame(df_bivar[y])
			# percentChar = '\%'
			# if df_bivar_num[y].astype(str).str.contains(percentChar).any() :
			df_bivar_num[y] = df_bivar_num[y].replace('\%','',regex=True).astype(float)
			df_bivar_num[y] = df_bivar_num[y].replace('\$','',regex=True).astype(float)
			df_bivar_num.fillna(0,inplace = True)
			# Excluding the numeric columns---
			df_bivar_cat = df_bivar.select_dtypes(exclude = ["number"])
			df_bivar_cat = df_bivar_cat.fillna('Missing/NA')
			df_bivar_cat = pd.DataFrame(df_bivar_cat[x])
			df_out = pd.concat([df_bivar_cat, df_bivar_num], axis=1, sort=False)
			df_out_sum = round((df_out.groupby([x])[y].sum().reset_index()),5)
			df_out_mean = round((df_out.groupby([x])[y].mean().reset_index()),5)
			# Creating dictionary from the dataframe---
			response_sum = json.loads(json_util.dumps(df_out_sum))
			dict_sum = json.dumps(response_sum)
			my_dict_sum = json.loads(dict_sum)
			key1 = ['Sum']
			val1 = [my_dict_sum]
			keyval1 = dict(zip(key1,val1))

			response_mean = json.loads(json_util.dumps(df_out_mean))
			dict_mean = json.dumps(response_mean)
			my_dict_mean = json.loads(dict_mean)
			key2 = ['Mean']
			val2 = [my_dict_mean]
			keyval2 = dict(zip(key2,val2))

			my_dict = {**keyval1,**keyval2}
			return my_dict
		else:
			return {"errors":"failed to save the file"}



	if request.method == "GET":
		if request.GET.get('method') == 'categorical bivariate' :
			try:
				respBivarCat = bivar_analysis_cat(request.GET.get('cat1'),request.GET.get('cat2'),request.GET.get('dataset'))
				return Response(respBivarCat)
			except Exception as e:
				print(e)
				return Response("Error in Categorical Bivariate analysis",status=status.HTTP_400_BAD_REQUEST)
		elif request.GET.get('method') == 'numeric bivariate' :
			try:
				respBivarNum = bivar_analysis_num(request.GET.get('num1'),request.GET.get('num2'),request.GET.get('dataset'))
				return Response(respBivarNum)
			except Exception as e:
				print(e)
				return Response("Error in Numeric Bivariate analysis",status=status.HTTP_400_BAD_REQUEST)
		elif request.GET.get('method') == 'bivariate sum' :
			try:
				respBivarCatSum = bivar_sum(request.GET.get('cat'),request.GET.get('num').split(','),request.GET.get('dataset'))
				return Response(respBivarCatSum)
			except Exception as e:
				print(e)
				return Response("Error in cat-num Bivariate analysis(sum)",status=status.HTTP_400_BAD_REQUEST)
		elif request.GET.get('method') == 'bivariate mean' :
			try:
				respBivarCatMean = bivar_mean(request.GET.get('cat'),request.GET.get('num').split(','),request.GET.get('dataset'))
				return Response(respBivarCatMean)
			except Exception as e:
				print(e)
				return Response("Error in cat-num Bivariate analysis(mean)",status=status.HTTP_400_BAD_REQUEST)
		elif request.GET.get('method') == 'bivariate sum mean' :
			try:
				respBivarCatMeanSum = bivar_sum_mean(request.GET.get('cat'),request.GET.get('num').split(','),request.GET.get('dataset'))
				return Response(respBivarCatMeanSum)
			except Exception as e:
				print(e)
				return Response("Error in cat-num Bivariate analysis(sum-mean)",status=status.HTTP_400_BAD_REQUEST)
	else:
		return Response("Error in GET request",status=status.HTTP_400_BAD_REQUEST)
