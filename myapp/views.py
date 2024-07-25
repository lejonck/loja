from django.shortcuts import render, redirect
from django.db import transaction
from .models import Produto, Pedido, ItemPedido
from django.shortcuts import render, get_object_or_404

def home_view(request):
    # Filtra produtos por categoria se o parâmetro de categoria estiver presente na URL
    categoria = request.GET.get('categoria')
    query = request.GET.get('query')
    if categoria:
        produtos = Produto.objects.filter(categoria=categoria)     
    elif query:
        produtos = Produto.objects.filter(nome__icontains=query)
    else:
        produtos = Produto.objects.all()
    
    
    return render(request, 'myapp/home.html', {'produtos': produtos, 'tem_produtos': produtos.exists()})

def produto_detalhes_view(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    return render(request, 'myapp/produto_detalhes.html', {'produto': produto})

def carrinho_view(request):
    carrinho = request.session.get('carrinho', {})
    produtos = Produto.objects.filter(id__in=carrinho.keys())
    total = 0
    for produto in produtos:
        quantidade = carrinho.get(str(produto.id))
        total += produto.preco * quantidade
    return render(request, 'myapp/carrinho.html', {'produtos': produtos, 'carrinho': carrinho, 'total': total})

def adicionar_ao_carrinho(request, produto_id):
    produto = Produto.objects.get(id=produto_id)
    carrinho = request.session.get('carrinho', {})
    if str(produto.id) in carrinho:
        carrinho[str(produto.id)] += 1
    else:
        carrinho[str(produto.id)] = 1
    request.session['carrinho'] = carrinho
    return redirect('carrinho')

def atualizar_quantidade(request, produto_id):
    if request.method == 'POST':
        quantidade = int(request.POST.get('quantidade'))
        carrinho = request.session.get('carrinho', {})
        if quantidade > 0:
            carrinho[str(produto_id)] = quantidade
        else:
            carrinho.pop(str(produto_id), None)
        request.session['carrinho'] = carrinho
    return redirect('carrinho')

def remover_do_carrinho(request, produto_id):
    carrinho = request.session.get('carrinho', {})
    carrinho.pop(str(produto_id), None)
    request.session['carrinho'] = carrinho
    return redirect('carrinho')

@transaction.atomic
def finalizar_pedido(request):
    if request.method == 'POST':
        carrinho = request.session.get('carrinho', {})
        if not carrinho:
            return redirect('carrinho')

        # Calcular o total do pedido
        total = 0
        for produto_id, quantidade in carrinho.items():
            produto = Produto.objects.get(id=produto_id)
            total += produto.preco * quantidade

        # Criar o pedido
        pedido = Pedido.objects.create(total=total)

        # Criar os itens do pedido
        for produto_id, quantidade in carrinho.items():
            produto = Produto.objects.get(id=produto_id)
            ItemPedido.objects.create(
                pedido=pedido,
                produto=produto,
                quantidade=quantidade,
                preco=produto.preco
            )

        # Limpar o carrinho
        request.session['carrinho'] = {}

        # Redirecionar para uma página de confirmação
        return redirect('confirmacao_pedido')

    return redirect('carrinho')

def confirmacao_pedido(request):
    return render(request, 'myapp/confirmacao_pedido.html')