from django.urls import path
from .views import home,upload,external

urlpatterns = [
    path('', home,name='home'),
    path('process/', external,name='proccessing...'),
    path('upload/', upload, name='upload'),
]
