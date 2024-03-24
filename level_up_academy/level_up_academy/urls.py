"""
URL configuration for level_up_academy project.

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
from django.urls import path
from django.conf.urls.static import static
from admin_panel import views

from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.create_word, name = 'dash'),
    path('login', views.login_user, name = 'login'),
    path('dash1/<int:id>', views.create_word2, name = 'dash2'),
    path('dash2/<int:id>', views.create_word3, name = 'dash3'),
    path('dash3/<int:id>', views.word_finish, name = 'dash4'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


