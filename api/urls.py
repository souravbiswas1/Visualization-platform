from django.contrib import admin
from django.urls import path,include
from rest_framework.authtoken.views import obtain_auth_token
from django.contrib import admin
from django.conf.urls import url
from django.urls import include, path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.routers import SimpleRouter

from . import univariate,columns_type,bivariate,multivariate,correlation,file_upload,descriptive_stat_Func,descriptive_stat_Class


schema_view = get_schema_view(
   openapi.Info(
      title="Vis APIs",
      default_version='v0.0.1',
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

router = SimpleRouter()

urlpatterns = [
    url(r'^$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('getUnivar', univariate.getUnivar),
    path('getColType', columns_type.getColType),
    path('getBivar', bivariate.getBivar),
    path('getMultivar', multivariate.getMultivar),
    path('getCorrelation', correlation.getCorrelation),
    path('getUploadfile', file_upload.getUploadfile),
    path('getDescriptive', descriptive_stat_Func.getDescriptive),
    path('getDescriptive', descriptive_stat_Class.getDescriptive),
]
