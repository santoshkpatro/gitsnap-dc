from django.urls import re_path, path
from .views import TreeView

urlpatterns = [
    re_path(r'^(?P<path>.*?)/?$', TreeView.as_view(), name='tree-view'),
]