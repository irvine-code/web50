from django.shortcuts import render,redirect
from .forms import RegisterForm,ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.
def register(request):
    if(request.method=='POST'):
       form=RegisterForm(request.POST)
       if form.is_valid():
          form.save()
          messages.success(request,f'Account Created.')
          return redirect('login')
    else:
       form=RegisterForm()
    return render(request,'network/register.html',{'form':form})
    
@login_required   
def profile(request):
    return render(request,'network/profile.html')
    
def profileupdate(request):
 if (request.method=='POST'):
   pform=ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
   if pform.is_valid:
      pform.save()
      return redirect('profile')
 else:
    pform=ProfileUpdateForm(instance=request.user.profile)
 return render(request,'network/profileupdate.html',{'pform':pform})


@login_required
def Search(request):
    if request.method == 'POST':
        kerko = request.POST.get('search')
        print(kerko)
        results = User.objects.filter(username__contains=kerko)
        context = {
            'results':results
        }
        return render(request, 'network/search_result.html', context)