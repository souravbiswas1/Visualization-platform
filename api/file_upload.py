from django.core.files.storage import FileSystemStorage
import json
from bson import json_util
from django.shortcuts import render
from rest_framework.decorators import api_view,renderer_classes
from rest_framework.response import Response
from rest_framework import status
import pickle
import shutil, os
from django.conf import settings
MEDIA_FOLDER_PATH = settings.MEDIA_ROOT + '\\'


@api_view(['POST'])
def getUploadfile(request):
	def upload_file(file_name):
		fs = FileSystemStorage()
		# save file data
		filename = fs.save(file_name.name, file_name)
		# get the path of file storage
		filepath = MEDIA_FOLDER_PATH + file_name.name
		if os.path.exists(filepath):
			return {"file_name": filename}
		else :
			return {"errors":"failed to save the file"}

		# uploaded_file_url = fs.url(filename)

	if request.method == "POST":
		try:
			resp = upload_file(request.FILES['source'])
			return Response(resp)
		except Exception as e:
			print(e)
			# exc_type, exc_obj, exc_tb = sys.exc_info()
			# fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			# print(exc_type, fname, exc_tb.tb_lineno)
			return Response("Error in uploading the data",status = status.HTTP_400_BAD_REQUEST)
	else:
		return Response("Error in POST request",status = status.HTTP_400_BAD_REQUEST)


