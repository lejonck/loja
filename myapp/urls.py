from django.urls import path
from . import views

#As URLs são mapeadas para as views correspondentes
#'path' é a função que define padrões de url. Quando essa URL especificada for chamada, direciona para a view correspondente

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
