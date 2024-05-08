from django.contrib import admin
from django.urls import path
from my_work import views

urlpatterns = [
    path("home/",views.HomePage.as_view(),name="home_1"),

    path("add/",views.AddUser.as_view(),name="add"),
    path("add_admin/",views.AddAdmin.as_view(),name="admin"),
    path("add_driver/",views.AddDriver.as_view(),name="driver"),

    path("createbin/",views.CreateGarbage.as_view(),name="create_garbage"),
    path("updatebin/<int:pk>",views.UpdateBin.as_view(),name="update_garbage"),
    path("G_viwe/",views.GarbageView.as_view(),name="Gviwe"),
    path("deletebin/<int:pk>",views.DeleteBin.as_view(),name="delete_garbage"),

    path("progress/",views.DailyProgress.as_view(),name="progress"),

    path("publiclist/",views.UsersList.as_view(),name="userlist"),
    path("driverlist/",views.DriverList.as_view(),name="driver_list"),

    path("complaintlist/",views.ComplaintView.as_view(),name="compliantlist"),

    path("Addarea/",views.AddLocation.as_view(),name="area"),

    path("logout/",views.Signout.as_view(),name="lgout") ,
    path("login",views.CustomLoginView.as_view(),name="lgn"),

    path("lcn/",views.LocationsView.as_view(),name="location"),
    path("deletelocation/<int:pk>",views.DeleteLocation.as_view(),name="delete_location"),

    
    
  

]