from django import views
from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import register, ProjectListView, PublicationListView, ProfileListView, DeleteProject, UpdateProject, CreateProject, UpdatePublications, PublicationDetailView

urlpatterns = [
    path('', ProjectListView.as_view(), name='home'),
    path('register/', register, name='register'),
    path('project/<str:project>', PublicationListView.as_view(), name='project'),
    path('publication/<pk>', PublicationDetailView.as_view(), name='publication'),
    path('publication/update/<str:project>', UpdatePublications, name='updatepublication'),
    path('profile/', login_required(ProfileListView.as_view()), name='profile'),
    path('update/<pk>', login_required(UpdateProject.as_view()), name='updateproject'),
    path('create/', login_required(CreateProject.as_view()), name='createproject'),
    path('delete/<pk>', login_required(DeleteProject.as_view()), name='deleteproject')
]
