from django.urls import path

from .views import GetDataList


urlpatterns = [
    path('list/', GetDataList.as_view(), name='list')
]
