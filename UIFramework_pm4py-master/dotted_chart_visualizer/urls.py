from django.urls import path
from . import views


urlpatterns = [
    path('', views.dcv, name='dotted-chart-visualizer'),



]
