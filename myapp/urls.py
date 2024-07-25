

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('produto/<int:produto_id>/', views.produto_detalhes_view, name='produto_detalhes'),
    path('carrinho/', views.carrinho_view, name='carrinho'),
    path('adicionar_ao_carrinho/<int:produto_id>/', views.adicionar_ao_carrinho, name='adicionar_ao_carrinho'),
    path('atualizar_quantidade/<int:produto_id>/', views.atualizar_quantidade, name='atualizar_quantidade'),
    path('remover_do_carrinho/<int:produto_id>/', views.remover_do_carrinho, name='remover_do_carrinho'),
    path('finalizar_pedido/', views.finalizar_pedido, name='finalizar_pedido'),
    path('confirmacao_pedido/', views.confirmacao_pedido, name='confirmacao_pedido'),
  
]
