

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
        path('produto/<int:produto_id>/', views.produto_detalhes_view, name='produto_detalhes'),
  
]
