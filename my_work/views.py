from django.shortcuts import render,redirect
from django.views.generic import View,CreateView,FormView,TemplateView
from my_work.forms import UserForm,GarbageBinForm
from my_work.models import User,GarbageBin,Complaint,Area,CollectionRequest,RequestTable
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from my_work.forms import CustomAuthenticationForm,AddLocationForm,AdminForm
from django.contrib.auth import authenticate,login,logout
from django.utils.decorators import method_decorator

def signin_requerd(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            return redirect("lgn")
        else:
            return fn(request,*args,**kwargs)
    return wrapper

class IndexPage(TemplateView):
    template_name="registration/base.html"

@method_decorator(signin_requerd,name="dispatch") 
class HomePage(TemplateView):
    template_name="registration/index.html"



class AddAdmin(View):
    def get(self, request, *args, **kwargs):
        form = AdminForm()
        
        return render(request, "registration/admin.html", {"form": form, })

    def post(self, request, *args, **kwargs):
        form = UserForm(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            return redirect('lgn')
        else:
            
            return render(request, "registration/admin.html", {"form": form, })
        
class AddDriver(View):
    def get(self, request, *args, **kwargs):
        form = AdminForm()
        
        return render(request, "registration/driver.html", {"form": form, })

    def post(self, request, *args, **kwargs):
        form = UserForm(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            return redirect('home_1')
        else:
            
            return render(request, "registration/driver.html", {"form": form, })


class AddUser(View):
    def get(self, request, *args, **kwargs):
        form = UserForm()
        areas = Area.objects.all()  # Fetch all Area objects
        return render(request, "registration/user.html", {"form": form, "areas": areas})

    def post(self, request, *args, **kwargs):
        form = UserForm(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            return redirect('lgn')
        else:
            areas = Area.objects.all()  # Fetch all Area objects
            return render(request, "registration/user.html", {"form": form, "areas": areas})

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'  
    success_url = 'your_success_url'

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        if user.user_type == 'admin':
            return redirect('home_1')  
        elif user.user_type == 'customer':
            return redirect('home_2')  
        elif user.user_type == 'driver':
            return redirect('home_3')  
        else:
            return redirect(self.success_url)
        

@method_decorator(signin_requerd,name="dispatch")
class CreateGarbage(View):
    def get(self,request,*args,**kwargs):
        form=GarbageBinForm()
        return render(request,"registration/garbage_create.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form = GarbageBinForm(request.POST)
        if form.is_valid():
                GarbageBin.objects.create(**form.cleaned_data)
                return redirect("home_1")
        
@method_decorator(signin_requerd,name="dispatch")
class UpdateBin(View):
    def get(self,request,*args,**kwargs):
        id = kwargs.get("pk")
        data = GarbageBin.objects.get(id=id)
        form = GarbageBinForm(instance=data)
        return render(request,"registration/garbage_update.html",{"form":form})
    

    def post(self,request,*args,**kwargs):
        id = kwargs.get("pk")
        data = GarbageBin.objects.get(id=id)
        form = GarbageBinForm(request.POST,instance=data)
        if form.is_valid():
            form.save()
            return redirect("home_1")
        
@method_decorator(signin_requerd,name="dispatch")
class DeleteBin(View):
     def get(self,request,*args,**kwargs):
          id = kwargs.get("pk")
          data = GarbageBin.objects.get(id=id).delete()
          return redirect("Gviwe")
     


@method_decorator(signin_requerd,name="dispatch")
class UsersList(View):
    def get(self, request, *args, **kwargs):
        data = User.objects.filter(user_type='customer')
        return render(request, "registration/userlist.html", {"data": data})
    
@method_decorator(signin_requerd,name="dispatch")
class DriverList(View):
    def get(self, request, *args, **kwargs):
        data = User.objects.filter(user_type='driver')  
        return render(request, "registration/driver_list.html", {"data": data})
    
@method_decorator(signin_requerd,name="dispatch")
class ComplaintView(View):
    def get(self,request,*args,**kwargs):
        data=Complaint.objects.filter(accepted=False,rejected=False)
        return render(request,"registration/complait_view.html",{"data":data})


@method_decorator(signin_requerd,name="dispatch")
class AddLocation(View):
    def get(self,request,*args,**kwargs):
        form=AddLocationForm()
        return render (request,"registration/area.html",{"form":form})
    def post(sel,request,*args,**kwargs):
        form = AddLocationForm(request.POST)
        if form.is_valid():
            Area.objects.create(**form.cleaned_data)
            return render (request,"registration/area.html",{"form":form})
            
@method_decorator(signin_requerd,name="dispatch")
class Signout (View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect('lgn')
    
@method_decorator(signin_requerd,name="dispatch")
class GarbageView(View):
    def get(self,request,*args,**kwargs):
        data=GarbageBin.objects.all()
        return render (request,"registration/garbage.html",{"data":data})
    
@method_decorator(signin_requerd,name="dispatch")
class LocationsView(View):
    def get(self,request,*args,**kwargs):
        data=Area.objects.all()
        return render (request,"registration/Location.html",{"data":data})
    

@method_decorator(signin_requerd,name="dispatch")
class DeleteLocation(View):
     def get(self,request,*args,**kwargs):
          id = kwargs.get("pk")
          data = Area.objects.get(id=id).delete()
          return redirect("location")



@method_decorator(signin_requerd,name="dispatch")
class DailyProgress(View):
    def get(self,request,*args,**kwargs):
        data = CollectionRequest.objects.filter(accepted=False)
        return render(request,"registration/progress.html",{"data":data})





        
                
