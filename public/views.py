from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView,View,CreateView,ListView
from public.forms import UserGarbageBinForm,ComplaintForm,userform
from my_work.models import Area, UserGarbageBin,Complaint, CollectionRequest,GarbageBin,RequestTable
from django.urls import reverse_lazy
from django.contrib import messages
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
    template_name="public/home.html"
    



@method_decorator(signin_requerd,name="dispatch") 
class RequestBin(CreateView):
    template_name='public/bin_request.html'
    
    form_class=UserGarbageBinForm
    model=UserGarbageBin
    success_url=reverse_lazy('home_2')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = GarbageBin.objects.all()  # Fetch all Area objects
        return context

    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)
              
    

@method_decorator(signin_requerd,name="dispatch") 
class AcceptRequestView(View):
    def post(self, request, pk):
        user_garbage_bin = get_object_or_404(UserGarbageBin, pk=pk)
        user_garbage_bin.status = 'accepted'
        user_garbage_bin.save()   
        return redirect('pending_requests')
@method_decorator(signin_requerd,name="dispatch") 
class RejectRequestView(View):
    def post(self, request, pk):
        user_garbage_bin = get_object_or_404(UserGarbageBin, pk=pk)
        user_garbage_bin.status = 'rejected'
        user_garbage_bin.save()
        return redirect('pending_requests')
# @method_decorator(signin_requerd,name="dispatch")    
def pending_requests_view(request):
    pending_requests = UserGarbageBin.objects.filter(status='pending')
    return render(request, 'public/pending_requests.html', {'pending_requests': pending_requests})


# @method_decorator(signin_requerd,name="dispatch") 
def send_complaint(request):
    if request.method == 'POST':
        issue = request.POST.get('issue', '')
        if issue:
            complaint = Complaint.objects.create(user=request.user, issue=issue)
            
            return redirect('home_2')  
        else:
            return redirect('home_2')          
    return render(request, 'public/send_complaint.html')  
@method_decorator(signin_requerd,name="dispatch") 
def view_complaint(request, complaint_id):
    complaint = Complaint.objects.get(id=complaint_id)
    if request.user == complaint.user:  
        return render(request, 'public/view_complaint.html', {'complaint': complaint})
    else:
        
        return redirect('home_2')  

# @method_decorator(signin_requerd,name="dispatch") 
def accept_complaint(request, complaint_id):
    complaint = Complaint.objects.get(id=complaint_id)
    if complaint.accepted== False:
       complaint.accepted = True
       complaint.save()
       return redirect("home_1")

# @method_decorator(signin_requerd,name="dispatch") 
def reject_complaint(request, complaint_id):
    complaint = Complaint.objects.get(id=complaint_id)
    if complaint.rejected== False:
       complaint.rejected = True
       complaint.save()
       return redirect("home_1")


# @method_decorator(signin_requerd,name="dispatch") 
def list_complaints(request):
    user_complaints = Complaint.objects.filter(user=request.user)
    return render(request, 'public/list_complaints.html', {'user_complaints': user_complaints})




@method_decorator(signin_requerd,name="dispatch") 
class CollectionRequestDetailView(TemplateView):
    template_name = 'public/detailstemplate.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_location = self.request.user.location  
        user_id = self.request.user.id
        bins = UserGarbageBin.objects.filter(user=user_id)
        
        for i in bins:
            collection_requests = CollectionRequest.objects.filter(
                area=user_location,  
                bin_id=i.bin.id,
                accepted=False
        )

        context['collection_request'] = collection_requests
        return context


@method_decorator(signin_requerd,name="dispatch") 
class ConformRequest(CreateView):
    template_name = 'public/collection_conform.html'
    form_class = userform
    model = RequestTable
    success_url = reverse_lazy('home_2')

    def form_valid(self, form):
        id = self.kwargs.get('pk')
        form.instance.user = self.request.user
        form.instance.request_id = id  
        return super().form_valid(form)    

@method_decorator(signin_requerd,name="dispatch") 
class Taskupdate(View):
    def get(self,request,*args,**kwargs):
        form=userform()
        id=kwargs.get("pk")
        qs=RequestTable.objects.get(id=id)
        if qs.result == True:
            qs.result = False
            qs.save()
        return redirect("home_2")
    
@method_decorator(signin_requerd,name="dispatch") 
class BinView(View):
    def get(self,request,*args,**kwargs):
        data=GarbageBin.objects.all()
        return render(request,"public/bin.html",{"data":data})
    


@method_decorator(signin_requerd,name="dispatch") 
class MyBin(View):
    def get (self,request,*args,**kwargs):
        user=self.request.user.id
        qs=UserGarbageBin.objects.filter(user_id=user)
        return render(request, "public/bindetails.html", {"qs":qs})
    

@method_decorator(signin_requerd,name="dispatch") 
class PaymentView(View):
    def get(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        data = RequestTable.objects.filter(id=id)
        qs = CollectionRequest.objects.filter(id__in=[i.request_id for i in data])
        det = GarbageBin.objects.filter(id__in=[k.bin_id for k in qs])
        
        
        return render(request, "public/payment.html", { "det": det, "qs": qs })
    
@method_decorator(signin_requerd,name="dispatch") 
class PaymentDetails(View):
    def get(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        data = RequestTable.objects.filter(id=id,)
        qs = CollectionRequest.objects.filter(id__in=[i.request_id for i in data])
        det = GarbageBin.objects.filter(id__in=[k.bin_id for k in qs])
        
        
        return render(request, "public/paymentdetails.html", { "det": det, "qs": qs })
    

@method_decorator(signin_requerd,name="dispatch") 
class CollectionHistory(View):
    def get(self,request,*args,**kwargs):
        id=self.request.user.id
        data=RequestTable.objects.filter(user_id=id).order_by('status')
        for i in data:
            qs=CollectionRequest.objects.filter(id=i.request_id)
            for k in qs:
                value=Area.objects.filter(id=k.area_id)
                details=GarbageBin.objects.filter(id=k.bin_id)
        return render(request,"public/paybill.html",{"data":data,"qs":qs,"value":value,"details":details})


    




    







        





   



    












