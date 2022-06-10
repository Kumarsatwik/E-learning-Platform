"""onlinecourses URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path,include
from . import settings
from courses import views
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('course/<str:slugs>',views.coursePage,name="course"),
    path('signup',views.signup.as_view(),name='signup'),
    path('login',views.login.as_view(),name="login"),
    path('logout',views.signout,name="logout"),
    path('mycourse',views.my_course,name="mycourse"),
    path('checkout/<str:slugs>',views.checkout,name="checkout"),
    path('verify_payment',views.verify_payment,name="verify"),
    path('',views.sample,name="home"),
    path('search',views.search_course,name='search_course'),
    path('profile',views.myprofile,name='profile'),
    path('wishlist/<str:slugs>',views.wishlist,name='wishlist'),
    path('download/<slug:order>',views.receipt,name='receipt'),
    path('review/<int:course_id>',views.review_rate,name="review")
]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
urlpatterns +=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)