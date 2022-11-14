from django.urls import path

from . import views

urlpatterns = [
    path('', views.IssueListView.as_view(), name='issue-list-view'),
    path('create/', views.IssueCreateView.as_view(), name='issue-create-view'),
    path('<int:number>/', views.IssueDetailView.as_view(), name='issue-detail-view'),
    path('<int:number>/close/', views.IssueCloseView.as_view(), name='issue-close-view'),
    path('<int:number>/open/', views.IssueOpenView.as_view(), name='issue-open-view'),
    path('<int:number>/comments/create/', views.IssueCommentCreateView.as_view(), name='issue-comment-create-view'),
]