from django.urls import re_path
from .views import BlobView


urlpatterns = [
    re_path(r'^(?P<path>.*?)/?$', BlobView.as_view(), name='blob-view'),
]