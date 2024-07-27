from django.shortcuts import render, redirect
from django.db import transaction
from .models import Produto, Pedido, ItemPedido
from django.shortcuts import render, get_object_or_404


# As function-based views recebem um HTTP request como entrada e devolvem um HTTP response

def home_view(request):
    categoria = request.GET.get('categoria')
    query = request.GET.get('query')
    marcas = request.GET.getlist('marcas')
    preco_max = request.GET.get('preco_max')

    produtos = Produto.objects.all()
    marcas_unicas = list(set(marcas))
    
    contagem_marcas = {marca: marcas.count(marca) for marca in marcas_unicas}
    marcas_impares = [marca for marca, contagem in contagem_marcas.items() if contagem % 2 != 0]

    if categoria:
        produtos = produtos.filter(categoria=categoria)     
    if query:
        produtos = produtos.filter(nome__icontains=query)
    if preco_max:
        produtos = produtos.filter(preco__lte=preco_max)
    if marcas:  
        produtos = produtos.filter(marca__in=marcas_impares)   
    
    return render(request, 'myapp/home.html', {'produtos': produtos, 'tem_produtos': produtos.exists(), 'marcas_selecionadas' : marcas_impares})

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

        
        total = 0
        for produto_id, quantidade in carrinho.items():
            produto = Produto.objects.get(id=produto_id)
            total += produto.preco * quantidade

        
        pedido = Pedido.objects.create(total=total)

        
        for produto_id, quantidade in carrinho.items():
            produto = Produto.objects.get(id=produto_id)
            ItemPedido.objects.create(
                pedido=pedido,
                produto=produto,
                quantidade=quantidade,
                preco=produto.preco
            )

        
        request.session['carrinho'] = {}

        
        return redirect('confirmacao_pedido')

    return redirect('carrinho')

def confirmacao_pedido(request):
    return render(request, 'myapp/confirmacao_pedido.html')