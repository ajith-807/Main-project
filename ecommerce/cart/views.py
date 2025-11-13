from django.shortcuts import render,redirect
from django.views import View
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from shop.models import Product
from cart.models import Cart
from cart.models import Order
from cart.forms import OrderForm
from django.contrib.auth import login
import razorpay

from cart.models import Order_items


# Create your views here.
class AddtoCart(View):
    def get(self,request,i):
        p=Product.objects.get(id=i)
        u=request.user
        try:
            c=Cart.objects.get(user=u,product=p) #checks whether the product already placed by the current user
            c.quantity+=1                           #or checks whether the product is there in the cart table
            c.save()                                #if yes increment the quantity by 1
        except:
            c=Cart.objects.create(user=u,product=p,quantity=1) #else create a new record in the cart table
            c.save()
        return redirect('cart:cartview')

class MinusCart(View):
    def get(self, request, i):
        p = Product.objects.get(id=i)
        u = request.user
        try:
            c = Cart.objects.get(user=u, product=p)  # checks whether the product already placed by the current user
            if c.quantity>1:
                c.quantity -=1  # or checks whether the product is there in the cart table
                c.save()
            else:
                c.delete()# if yes increment the quantity by 1
        except:
            pass
        return redirect('cart:cartview')

class CartDelete(View):
    def get(self,request,i):
        p = Product.objects.get(id=i)
        u = request.user
        c = Cart.objects.get(user=u, product=p)
        c.delete()
        return redirect('cart:cartview')

class CartView(View):
    def get(self,request):
        u=request.user
        c=Cart.objects.filter(user=u)
        total=0
        for i in c:
            total+=i.product.price*i.quantity
        context={'cart':c,'total':total}
        return render(request,'cart.html',context)

def checkstock(c):
    stock=True
    for i in c:
        if i.product.stock<i.quantity:
            stock=False
            break
    else:
        stock=True
    return stock
import uuid
class CheckoutView(View):
    def post(self,request):
        form_instance=OrderForm(request.POST)
        if form_instance.is_valid():
            o=form_instance.save(commit=False)
            u=request.user
            o.user=u
            c=Cart.objects.filter(user=u)
            total=0
            for i in c:
                total+=i.product.price*i.quantity
            o.amount=total
            o.save()
            if(o.payment_method=="online"):
                client=razorpay.Client(auth=('rzp_test_Rckx1UXGI7I63k','aDQ6ct8Kby4ExAYBt1njczUi'))
                print(client)
                #place order
                response_payment=client.order.create(dict(amount=total*100,currency='INR'))
                print(response_payment)
                id = response_payment['id']
                o.order_id=id
                o.save()
                context={'payment':response_payment}
                return render(request, 'payment.html', context)
            else :
                c = Cart.objects.filter(user=u)
                o.is_ordered = True
                uid=uuid.uuid4().hex[:14]
                id='order_COD'+uid
                o.order_id=id
                o.save()
                order=Order.objects.get(order_id=id)
                for i in c:
                    o = Order_items.objects.create(order=order, product=i.product, quantity=i.quantity)
                    o.save()
                    o.product.stock -= o.quantity
                    o.product.save()
                c.delete()
                return render(request, 'payment.html')

    def get(self,request):
        u=request.user
        c=Cart.objects.filter(user=u)
        print(c)

        stock=checkstock(c)
        if stock:

            form_instance=OrderForm()
            context={'form':form_instance}
            return render(request,'checkout.html',context)
        else:

            messages.error(request,"cant place order")
            return render(request,'checkout.html')

from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
@method_decorator(csrf_exempt,name="dispatch")
class Paymentsuccess(View):
    def post(self,request,i):
        print(i)
        u=User.objects.get(username=i)
        login(request,u)
        response=request.POST
        print(response)
        id=response['razorpay_order_id']
        print(id)
        order=Order.objects.get(order_id=id)
        order.is_ordered=True
        order.save()

        c=Cart.objects.filter(user=u)
        for i in c:
            o=Order_items.objects.create(order=order,product=i.product,quantity=i.quantity)
            o.save()
            o.product.stock-=o.quantity
            o.product.save()
        c.delete()
        return render(request,'paymentsuccess.html')

class YourOrders(View):
    def get(self,request):
        u=request.user
        o=Order.objects.filter(user=u,is_ordered=True)
        context={'order':o}
        return render(request,'yourorders.html',context)

