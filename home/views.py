from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from home.models import Item, Category, Price, SubCategory, OrderItem, Order
from account.models import Account
from django.http import HttpResponse 
from django.views.generic import ListView, DetailView, View
import json
from django.utils.text import slugify
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.models import AnonymousUser

# Create your views here.
class HomeView(ListView):
    model = Category
    template_name = "home.html"
        
class CategoryView(DetailView):
    model = Category
    template_name = "category.html"
    def get_context_data(self, **kwargs):
        category = self.request.GET.get('c', None)
        # Call the base implementation first to get the context
        context = super(CategoryView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        area = "kkd_rural"
        PriceFiltered = Price.objects.filter(item__sub_category__category__category__in = [context['object']])
        if category is None:
            context['Area'] = PriceFiltered.only("item", area+"_p", area+"_dp")
        else:
            context['Area'] = PriceFiltered.filter(item__sub_category__sub_category__in =[category]).only("item", area+"_p", area+"_dp")
            context['curr'] = category
        context['sub_c'] = SubCategory.objects.filter(category=context['object'])
        slugs = {}
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            for item in order.items.all():
                slugs[getattr(item.item.item, "slug")] = getattr(item, "quantity")
            context['slugs'] = slugs
        except ObjectDoesNotExist:
            pass
        except TypeError:
            pass
        return context

class OrderSummaryView(LoginRequiredMixin, View):
    login_url = '/account/login/'
    redirect_field_name = 'next'
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            area = "kkd_rural"
            total, saved = 0, 0
            
            for item in order.items.all():
                item.price = getattr(item.item, area+"_p")
                item.discounted_price = getattr(item.item, area+"_dp")
                item.save()
                if(item.discounted_price):
                    total+=item.get_total_discount_item_price()
                    saved+=item.get_amount_saved()
                else:
                    total+=item.get_total_item_price()
            order.total_amount = total
            order.amount_saved = saved
            context = {
                'object': order
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")
        
def update_cart(request):
    return HttpResponse("<h1>Working<h1>")

#Ajax Functions
def add_to_cart(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Please Login First")
        next_url = "/account/login/?next="+request.GET.get('next', None)
        return HttpResponse(json.dumps({"Status": False, "next": next_url}), content_type="application/json")
    slug = request.GET.get('slug', None)
    quantity = request.GET.get('quantity', None)
    if slug is None:
        return HttpResponse(json.dumps({"Status": False}), content_type="application/json")
    item = get_object_or_404(Item, slug=slug)
    area = get_object_or_404(Price, item=item)
    order_item, created = OrderItem.objects.get_or_create(item = area, user = request.user, ordered = False)
    order_item.quantity = int(quantity)
    order_item.save()
    order_qs = Order.objects.filter(user = request.user, ordered = False)
    if(quantity == '0'):
        order_item.delete()
        count = order_qs[0].items.count()
        if(order_qs.exists() and order_qs[0].items.count() == 0):
            order_qs[0].delete()
        return HttpResponse(json.dumps({"Status": False, "count": count}), content_type="application/json")
    
    if(order_qs.exists()):
        if(not order_qs[0].items.filter(item__item__slug = slugify(slug)).exists()):
            order_qs[0].items.add(order_item)
    else:
        order = Order.objects.create(user = request.user)
        order.items.add(order_item)
    return HttpResponse(json.dumps({"Status": True, "count": order_qs[0].items.count()}), content_type="application/json")