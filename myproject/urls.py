"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import include, path
from myapp.views import HelloWorld, Async_page, PageTwo, PageThree, GraphPage, my_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HelloWorld.as_view(), name='hello_world_cbv'),
    path('two', PageTwo.as_view(), name='PageTwo_cbv'),
    path('PageThree/', PageThree, name='PageThree'),
    path('graph/', GraphPage, name='GraphPage'),
    path('view/', my_view, name='my_view'),
    path('async_page/', Async_page, name='Async_page'),
]

# MEDIA_URL = '/media/'
#
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


