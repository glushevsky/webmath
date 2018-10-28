from django.urls import path
from graph.views import base, data_processing

urlpatterns = [
    path('', base),
    path('data_processing', data_processing)
]
