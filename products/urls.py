"""ecart URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from os import name
from django.urls import path
from django.conf.urls.static import static
from . import views

from django.conf import settings

urlpatterns = [
    path('',views.index,name='home'),
    path('product_list',views.product_list,name='product_list'),
    path('product_detail/<id>',views.product_detail,name='product_detail'),
    path('account',views.show_account,name='account'),
    path('cart',views.show_cart,name='cart'),
    path('logout',views.signout,name='logout'),
    path('add_to_cart',views.add_to_cart,name='add_to_cart'),
    path('remove_item/<id>',views.remove_item,name='remove_item'),
    path('checkout',views.checkout_cart,name='checkout'),
    path('orders',views.view_orders,name='orders')
    
]

urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
