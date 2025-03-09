"""
URL configuration for LBPS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('system_admin/', admin.site.urls),
    path('', include('parking.urls')),
    path('', include('core.urls')),
    path('', include('authentication.urls')),
    path('', include('user.urls')),
    path('', include('city.urls')),
    path('', include('subcity.urls')),
    path('', include('woreda.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

