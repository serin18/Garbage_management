from django.contrib import admin
from django.urls import path
from driver import views

urlpatterns = [
    path("home/",views.HomePage.as_view(),name="home_3"),
    path("request/",views.CollectionRequestView.as_view(),name="rqst"),
    path("c_list/",views.ConformLstView.as_view(),name="conform"),
    path("status/<int:pk>",views.StatusUpdate.as_view(),name="status"),
    path("work/",views.DailyWork.as_view(),name="work"),
    path("daily/<int:pk>",views.DailyUpdate.as_view(),name="daily"),
    path("completed/",views.completedLstView.as_view(),name="complete")
    
    
]
