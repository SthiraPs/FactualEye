from django.urls import path
from . import views

urlpatterns = [
    path('mymodel/', views.my_model_list),
    path('mymodel/<int:id>', views.my_model_details),

]
