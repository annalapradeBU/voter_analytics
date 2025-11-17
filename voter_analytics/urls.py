# File: urls.py
# Author: Anna LaPrade (alaprade@bu.edu), 10/28/2025
# Description: the url patterns for voter_analytics app

from django.urls import path
from . import views 

urlpatterns = [
    path(r'', views.VotersListView.as_view(), name='home'),
    path(r'voters', views.VotersListView.as_view(), name='voters_list'),
    path('voter_analytics/voters/<int:pk>/', views.VoterDetailView.as_view(), name='voter_detail'),
    path('graphs/', views.GraphView.as_view(), name='graphs'),
]