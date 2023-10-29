"""
URL configuration for facutualeye project.

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
from django.urls import path, include
from core import views as core_views
from predict_area import views as predict_are_views
from rest_framework.urlpatterns import format_suffix_patterns

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('mymodel/', core_views.my_model_list),
#     path('mymodel/<int:id>', core_views.my_model_details),

#     path('predict-area/', predict_are_views.get_prediction),

# ]

# urlpatterns = format_suffix_patterns(urlpatterns)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('', include('predict_area.urls')),

]

urlpatterns = format_suffix_patterns(urlpatterns)
