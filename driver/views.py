from django.shortcuts import get_object_or_404, render,redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView,View,CreateView,ListView
from django.contrib import messages
from my_work.models import GarbageBin,CollectionRequest,Area,RequestTable
from my_work.models import *
from driver.forms import RquestForm
from public.forms import userform
from django.utils.decorators import method_decorator

def signin_requerd(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            return redirect("lgn")
        else:
            return fn(request,*args,**kwargs)
    return wrapper





@method_decorator(signin_requerd,name="dispatch")
class HomePage(TemplateView):
    template_name="driver/home.html"


@method_decorator(signin_requerd,name="dispatch")
class CollectionRequestView(CreateView):
    template_name='driver/col_request.html'
    form_class= RquestForm
    model=CollectionRequest
    success_url=reverse_lazy('home_3')
    areas = Area.objects.all()
    bin = GarbageBin.objects

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = GarbageBin.objects.all()
        context['qs'] = Area.objects.all()  # Fetch all Area objects
        return context

    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)
    

@method_decorator(signin_requerd,name="dispatch")
class ConformLstView(TemplateView):
    template_name = 'driver/conformlist.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.user.id
        data = CollectionRequest.objects.filter(user=user_id)
        
        collection_conform = []
        qs = []

        for i in data:
            conform_requests = RequestTable.objects.filter(
                request_id=i.id,
                result=True,
                status=False
            )
            collection_conform.extend(conform_requests)

        if not collection_conform:
            context['no_data_message'] = "No conforming requests found."
        else:
            for p in collection_conform:
                user = User.objects.filter(id=p.user_id).first()
                if user:
                    qs.append(user)

        if not qs:
            context['no_qs_message'] = "No corresponding users found for the conforming requests."

        context['collection_conform'] = collection_conform
        context['qs'] = qs
        return context


@method_decorator(signin_requerd,name="dispatch")
class StatusUpdate(View):
    def get(self,request,*args,**kwargs):
        form=userform()
        id=kwargs.get("pk")
        qs=RequestTable.objects.get(id=id)
        if qs.status == False:
            qs.status = True
            qs.save()
        elif qs.status == True:
            qs.status = False
            qs.save()
        return redirect("home_3")
    

@method_decorator(signin_requerd,name="dispatch")
class DailyWork(View):
    def get(self,request,*args,**kwargs):
        user_id=self.request.user.id
        data=CollectionRequest.objects.filter(
            user=user_id,
            accepted=False
        )
        return render(request,"driver/work.html",{"data":data})
    
@method_decorator(signin_requerd,name="dispatch")
class DailyUpdate(View):
    def get(self,request,*args,**kwargs):
        form=RquestForm()
        id=kwargs.get("pk")
        qs=CollectionRequest.objects.get(id=id)
        if qs.accepted == False:
            qs.accepted = True
            qs.save()
        elif qs.accepted == True:
            qs.accepted = False
            qs.save()
        return redirect("home_3")
    

@method_decorator(signin_requerd,name="dispatch")
class completedLstView(TemplateView):
    template_name = 'driver/completedlist.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.user.id
        data = CollectionRequest.objects.filter(user=user_id)
        
        collection_conform = []
        qs = []

        for i in data:
            conform_requests = RequestTable.objects.filter(
                request_id=i.id,
                result=True,
                status=True
            )
            collection_conform.extend(conform_requests)

        if not collection_conform:
            context['no_data_message'] = "No conforming requests found."
        else:
            for p in collection_conform:
                user = User.objects.filter(id=p.user_id).first()
                if user:
                    qs.append(user)

        if not qs:
            context['no_qs_message'] = "No corresponding users found for the conforming requests."

        context['collection_conform'] = collection_conform
        context['qs'] = qs
        return context
    






    









