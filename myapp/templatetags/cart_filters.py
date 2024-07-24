from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(str(key))

@register.simple_tag
def get_total(produto, carrinho):
    quantidade = carrinho.get(str(produto.id), 0)
    return produto.preco * quantidade
