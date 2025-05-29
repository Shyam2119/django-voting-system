from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('election/<int:election_id>/', views.election_detail, name='election_detail'),
    path('election/<int:election_id>/confirmation/', views.vote_confirmation, name='vote_confirmation'),
    path('election/<int:election_id>/results/', views.election_results, name='election_results'),
    path('verify/', views.verify_vote, name='verify_vote'),
]