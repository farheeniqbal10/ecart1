from django.shortcuts import render,redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
import customers
from customers.models import Customer
from orders.models import Order,OrderedItem
from . models import Product 
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from customers.models import Customer
from django.contrib import messages
from django.contrib.auth import authenticate,login

# Create your views here.
def index(request):
    featured=Product.objects.order_by('priority')[:4]
    latest=Product.objects.order_by('-id')[:4]
    return render(request,'index.html',{'featured':featured,'latest':latest})

def product_list(request):
    page=1
    if request.GET:
        page=request.GET.get('page',1)
    product_list=Product.objects.order_by('priority')
    product_paginator=Paginator(product_list,4)
    product_list=product_paginator.get_page(page)
    return render(request,'products.html',{'products':product_list})

def product_detail(request,id):
    product=Product.objects.get(id=id)
    return render(request,'product_detail.html',{'product':product})

def show_account(request):
    if request.POST and 'register' in request.POST:
        try:
            username=request.POST.get('username')
            email=request.POST.get('email')
            password=request.POST.get('password')
            address=request.POST.get('address')
            phone=request.POST.get('phone')

            user=User.objects.create_user(
                username=username,
                password=password,
                email=email
            )

            customer=Customer.objects.create(
                name=username,
                user=user,
                phone=phone,
                address=address
            )

            return redirect('account')
        except Exception as e:
            error_message="Duplicate username or invalid credentials"
            messages.error(request,error_message)

    if request.POST and 'login' in request.POST:
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)
        if user:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"invalid credentials")
                
    return render(request,"account.html")

def show_cart(request):
    user=request.user
    customer=user.customer_profile
    cart_obj,created=Order.objects.get_or_create(
            owner=customer,
            order_status=Order.CART_STAGE
        )

    return render(request,"cart.html",{'cart':cart_obj})

@login_required(login_url='account')
def add_to_cart(request):
    if request.POST:
        user=request.user
        customer=user.customer_profile
        quantity=int(request.POST.get('quantity'))
        product_id=request.POST.get('product_id')
        cart_obj,created=Order.objects.get_or_create(
            owner=customer,
            order_status=Order.CART_STAGE
        )
        product=Product.objects.get(id=product_id)

        ordered_item,created=OrderedItem.objects.get_or_create(
            product=product,
            owner=cart_obj,
        )
        if created:
            ordered_item.quantity=quantity
            ordered_item.save()

        else:
            ordered_item.quantity=ordered_item.quantity+quantity
            ordered_item.save()           
    return redirect('cart')

def checkout_cart(request):
    if request.POST:
        try:
            
                user=request.user
                customer=user.customer_profile
                total=float(request.POST.get('total'))
                order_obj=Order.objects.get(
                    owner=customer,
                    order_status=Order.CART_STAGE
                )
                if order_obj:
                    order_obj.order_status=Order.ORDER_CONFIRMED
                    order_obj.total_price=total
                    order_obj.save()
                    status_message="Your order is processed."
                    messages.success(request,status_message)
                else:
                    status_message="Your order is unable to process."
                    messages.error(request,status_message)
        except Exception as e:
            status_message="Your order is unable to process."
            messages.error(request,status_message)
    return redirect('cart')


def remove_item(request,id):
    item=OrderedItem.objects.get(id=id)
    if item:
        item.delete()
    return redirect('cart')

def signout(request):
    logout(request)
    return redirect('home')

@login_required(login_url='account')
def view_orders(request):
    user=request.user
    customer=user.customer_profile
    all_orders=Order.objects.filter(owner=customer).exclude(order_status=Order.CART_STAGE)
    
    return render(request,"orders.html",{'orders':all_orders})
    