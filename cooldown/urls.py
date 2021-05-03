"""cooldown URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views
from .views import SignUpView

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('',views.dashboard),
    path('char',views.character),
    path('use/<str:item>',views.use_item),
    path('recharge',views.recharge_item),
    path('cast/<str:spell>',views.cast_spell),
    path('take_turn',views.take_turn),
    path('rest',views.rest),
    path('a',views.a),
    path('admin',views.admin),
    path('d/<str:type>/<str:id>',views.delete),

    path('accounts/',include('django.contrib.auth.urls')), # login and signup features
    path('signup/',SignUpView.as_view(), name = 'signup'),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
