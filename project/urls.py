"""project URL Configuration

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
from django.contrib import admin
from django.urls import path
from app01.views import book, admin, account

urlpatterns = [
    # path('admin/', admin.site.urls),
    # 书籍信息管理
    path('book/list/', book.book_list),
    path('book/add/', book.book_add),
    path('book/<int:nid>/edit/', book.book_edit),
    path('book/<int:nid>/delete/', book.book_delete),
    # path('book/<int:nid>/sale', book.book_sale)

    # 管理员管理
    path('admin/list/', admin.admin_list),
    path('admin/add/', admin.admin_add),
    path('admin/<int:nid>/edit/', admin.admin_edit),
    path('admin/<int:nid>/delete/', admin.admin_delete),
    path('admin/<int:nid>/reset/', admin.admin_reset),

    # 登录与注销
    path('login/', account.login),
    path('logout/', account.logout),
]
