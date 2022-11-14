from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from gitsnap.pages.views import (
    index_view
)

from gitsnap.projects.views import (
    ProjectCreateView,
    ProjectDetailView
)

from gitsnap.commits.views import (
    CommitListView
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_view, name='index-view'),
    path('<str:username>/create/', ProjectCreateView.as_view(), name='project-create-view'),
    path('<str:username>/<str:name>/', ProjectDetailView.as_view(), name='project-detail-view'),
    path('<str:username>/<str:name>/issues/', include('gitsnap.issues.urls')),
    path('<str:username>/<str:name>/-/commits/<str:branch>/', CommitListView.as_view(), name='commit-list-view'),
    path('<str:username>/<str:name>/-/tree/<str:branch>/', include('gitsnap.tree.urls')),
    path('<str:username>/<str:name>/-/blob/<str:branch>/', include('gitsnap.blob.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)