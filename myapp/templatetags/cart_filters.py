from django import template

#As template tags são essas funções que podemos chamar nos templates, adicionando lógica nos templates de forma simples
#Existem as built-in tags que vêm como padrão com Django, como {% for %} e {% if %}

register = template.Library()

@register.filter
#Essa função retorna o valor associado a chave no dicionário  
def get_item(dictionary, key):
    return dictionary.get(str(key))

#Registra como uma template tag, que pode ter mais argumentos e lógica mais complexa
@register.simple_tag
#Recebe carrinho e produto como argumento, calcula o total do carrinho
def get_total(produto, carrinho):
    quantidade = carrinho.get(str(produto.id), 0)
    return produto.preco * quantidade
