from django.shortcuts import render
from django.views import View
from shop.models import Product
from django.db.models import Q
# Create your views here.
class SearchView(View):
    def get(self,request):
        query=request.GET['q']
        # print(query)
        if query:
            s=Product.objects.filter(
                Q(name__icontains=query)|Q(description__icontains=query)|Q(price__icontains=query)
            )
            context={'search':s}
            return render(request,'search.html',context)