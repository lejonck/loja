from django.db import models

#Os models definem a estrutura e comportamento dos dados e modelam para tabelas no banco de dados


class Produto(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.CharField(max_length=100)
    imagem = models.ImageField(upload_to='produtos/', blank=True, null=True)
    marca = models.CharField(max_length=100)

    #Esse método retorna uma string que representa esse modelo
    def __str__(self):
        return self.nome

class Pedido(models.Model):
    #Esse campo é preenchido automáticamente quando um Pedido é criado
    data_criacao = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)


class ItemPedido(models.Model):
    #Esse campo é chave estrangeira referenciando a tabela Pedidos. Se um Pedido for deletado, todos seus itens são também
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens')
    #Esse campo é chave estrangeira referenciando a tabela Produto. Se um Produto for deletado, os itens no pedido são também
    produto = models.ForeignKey('Produto', on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)

