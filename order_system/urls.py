"""
URL configuration for order_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

from django.contrib import admin
from django.urls import path, include
from orders.views import home_view, signup, login_view, manage_orders_view, complete_order_view, create_order_view, order_confirmation_view, custom_logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('', home_view, name='home'),
    path('manage-orders/', manage_orders_view, name='manage_orders'),
    path('complete-order/<int:order_id>/', complete_order_view, name='complete_order'),
    path('create-order/', create_order_view, name='create_order'),
    path('logout/', custom_logout, name='logout'),
    path('order-confirmation/<int:order_id>/', order_confirmation_view, name='order_confirmation'),

]