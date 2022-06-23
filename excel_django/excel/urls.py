from django.urls import path
from . import views

app_name    = "excel"
urlpatterns = [
    path('', views.index, name="index"),
    path('download/<int:pk>/', views.download, name="download"),
]
