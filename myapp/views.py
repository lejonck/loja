from django.shortcuts import render

from .models import Produto

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
    
    return render(request, 'myapp/home.html', {'produtos': produtos})

def produto_detalhes_view(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    return render(request, 'myapp/produto_detalhes.html', {'produto': produto})
