from django.shortcuts import render, redirect
from django.db import transaction
from .models import Produto, Pedido, ItemPedido
from django.shortcuts import render, get_object_or_404
from django import forms

#As views recebem um request como entrada e devolvem um response. Geralmente interagem com os models, 
#e podem renderizar templates HTML, além de outros tipos de resposta gerados
#Foram usadas as function-based views, que são funções em python que recebem um objeto HttpRequest e retornam um HttpResponse

#Formulário que usa o widget de CheckboxSeelectMultiple para escolher as marcas
class FiltroMarcaForm(forms.Form):
    MARCAS_CHOICES = [
        ('samsung', 'Samsung'),
        ('apple', 'Apple'),
        ('motorola', 'Motorola'),
        ('lenovo', 'Lenovo'),
        ('dell', 'Dell')
    ]
    
    marcas = forms.MultipleChoiceField(
        choices=MARCAS_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

def home_view(request):
    #Recebe os dados do request
    categoria = request.GET.get('categoria')
    query = request.GET.get('query')
    form = FiltroMarcaForm(request.GET or None)
    preco_max = request.GET.get('preco_max')

    produtos = Produto.objects.all()

    #Filtra pelos dados informados
    if categoria:
        produtos = produtos.filter(categoria=categoria)     
    if query:
        produtos = produtos.filter(nome__icontains=query)
    if preco_max:
        produtos = produtos.filter(preco__lte=preco_max)
    if form.is_valid():
        marcas_selecionadas = form.cleaned_data.get('marcas')
        if marcas_selecionadas:
            produtos = produtos.filter(marca__in=marcas_selecionadas)   
    #Renderiza o temlpate da home com o contexto dos produtos filtrados, o form e um booleano sehá ou não produtos
    return render(request, 'myapp/home.html', {'produtos': produtos, 'form': form, 'tem_produtos': produtos.exists()})

#Recebe o request com os dados da requisição http e o id do produto específico
def produto_detalhes_view(request, produto_id):
    #Recupera o produto, ou retorna uma página 404 de erro se não encotrar
    produto = get_object_or_404(Produto, id=produto_id)
    #Gera resposta http passando dicionário de contexto com o produto
    return render(request, 'myapp/produto_detalhes.html', {'produto': produto})


def carrinho_view(request):
    #Recebe o carrinho da sessão do usuário, se não existir criar dicionário vazio
    carrinho = request.session.get('carrinho', {})
    produtos = Produto.objects.filter(id__in=carrinho.keys())
    total = 0
    #Passa pelos produtos do carrinho e calcula o total
    for produto in produtos:
        quantidade = carrinho.get(str(produto.id))
        total += produto.preco * quantidade
    return render(request, 'myapp/carrinho.html', {'produtos': produtos, 'carrinho': carrinho, 'total': total})

def adicionar_ao_carrinho(request, produto_id):
    #Pega o produto pelo id e recupera o carrinho da sessão
    produto = Produto.objects.get(id=produto_id)
    carrinho = request.session.get('carrinho', {})
    #Se produto já está no carrinho, adiciona a quantidade, senão seta como 1
    if str(produto.id) in carrinho:
        carrinho[str(produto.id)] += 1
    else:
        carrinho[str(produto.id)] = 1
    #Atualiza a sessão com carrinho modificado      
    request.session['carrinho'] = carrinho
    #Já rediciona para a página do carrinho
    return redirect('carrinho')

def atualizar_quantidade(request, produto_id):
    if request.method == 'POST':
        #Obtém a quantidade informada no formulário POST
        quantidade = int(request.POST.get('quantidade'))
        carrinho = request.session.get('carrinho', {})
        # Atualiza o carrinho com a quantidade
        carrinho[str(produto_id)] = quantidade
        #Atualiza a sessão 
        request.session['carrinho'] = carrinho
    return redirect('carrinho')

def remover_do_carrinho(request, produto_id):
    #Recupera o carrinho da sessão
    carrinho = request.session.get('carrinho', {})
    #Remove a chave do dicionário, removendo o produto do carrinho
    carrinho.pop(str(produto_id), None)
    request.session['carrinho'] = carrinho
    return redirect('carrinho')

#Garante que todas as operações da função serão feitas em uma única transação
@transaction.atomic
def finalizar_pedido(request):
    if request.method == 'POST':
        #Recupera o carrinho da sessão
        carrinho = request.session.get('carrinho', {})
        if not carrinho:
            return redirect('carrinho') 
        #Calcula o total do pedido    
        total = 0
        for produto_id, quantidade in carrinho.items():
            produto = Produto.objects.get(id=produto_id)
            total += produto.preco * quantidade

        #Cria novo objeto Pedido no banco de dados com o total
        pedido = Pedido.objects.create(total=total)
        
        #Cria um objeto ItemPedido para cada item, associando ao Pedido já criado
        for produto_id, quantidade in carrinho.items():
            produto = Produto.objects.get(id=produto_id)
            ItemPedido.objects.create(
                pedido=pedido,
                produto=produto,
                quantidade=quantidade,
                preco=produto.preco
            )

        #Limpa o carrinho da sessão
        request.session['carrinho'] = {}

        #Retorna para a página de confirmação do pedido
        return redirect('confirmacao_pedido')

    #Se não for método POST, volta na página do carrinho
    return redirect('carrinho')

def confirmacao_pedido(request):
    #Renderiza a página que diz que o pedido foi confirmado
    return render(request, 'myapp/confirmacao_pedido.html')