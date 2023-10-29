from django.urls import path
from . import views

urlpatterns = [
    path('predict-area/', views.get_prediction),

]
