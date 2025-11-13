from django.shortcuts import render,redirect
from django.views import View
from shop.models import Category
from shop.forms import SignupForm,LoginForm,CategoryForm,ProductForm,StockForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
# Create your views here.
class Categoryview(View):
    def get(self,request):
        c=Category.objects.all()
        context={'category':c}
        return render(request,'categories.html',context)

class Productview(View):
    def get(self,request,i):
        c=Category.objects.get(id=i)
        context={'category':c}
        return render(request,'products.html',context)

from shop.models import Product
class Productdetails(View):
    def get(self,request,i):
        p=Product.objects.get(id=i)
        context={'product':p}
        return render(request,'productdetail.html',context)

class Register(View):
    def get(self,request):
        form_instance=SignupForm()
        context={'form':form_instance}
        return render(request,'register.html',context)

    def post(self,request):
        form_instance=SignupForm(request.POST)
        if form_instance.is_valid():
            form_instance.save()
            return redirect('shop:login')
        else:
            print(form_instance.errors)
            return render(request,'register.html',{'form':form_instance})

class Login(View):
    def post(self,request):
        form_instance=LoginForm(request.POST)
        if form_instance.is_valid():
            u=form_instance.cleaned_data['username']
            p=form_instance.cleaned_data['password']
            user=authenticate(username=u,password=p)

            if user and user.is_superuser==True:
                login(request,user)
                return redirect('shop:category')
            elif user and user.is_superuser!=True:
                login(request,user)
                return redirect('shop:category')
            else:
                messages.error(request,'invalid user credentials')
        return render(request,'login.html')
    def get(self,request):
        form_instance = LoginForm()
        context = {'form': form_instance}
        return render(request, 'login.html', context)
class Logout(View):
    def get(self,request):
        logout(request)
        return redirect('shop:login')

class AddCategory(View):
    def get(self,request):
        form_instance=CategoryForm()
        context= {'form': form_instance}
        return render(request,'Addcategory.html',context)
    def post(self,request):
        form_instance=CategoryForm(request.POST,request.FILES)
        if(form_instance.is_valid):
            form_instance.save()
            return render(request,'Addcategory.html')

class AddProduct(View):
    def get(self,request):
        form_instance=ProductForm()
        context= {'form': form_instance}
        return render(request,'Addproduct.html',context)
    def post(self,request):
        form_instance=ProductForm(request.POST,request.FILES)
        if(form_instance.is_valid):
            form_instance.save()
            return render(request,'Addproduct.html')

class Addstock(View):
    def get(self,request,i):
        p=Product.objects.get(id=i)
        form_instance = StockForm(instance=p)
        context= {'form': form_instance}
        return render(request,'stockform.html',context)
    def post(self,request,i):
        p = Product.objects.get(id=i)
        form_instance=StockForm(request.POST,instance=p)
        if(form_instance.is_valid):
            form_instance.save()
            return render(request,'stockform.html')
        else:
            print("error")
            return render(request,'stockform.html')
