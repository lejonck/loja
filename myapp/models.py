from django.db import models

#Models definem a estrutura e comportamento dos dados e modelam para tabelas no banco de dados

class Produto(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.CharField(max_length=100)
    imagem = models.ImageField(upload_to='produtos/', blank=True, null=True)
    marca = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Pedido(models.Model):
    data_criacao = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Pedido {self.id} - {self.data_criacao.strftime('%Y-%m-%d %H:%M:%S')}"

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey('Produto', on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantidade} x {self.produto.nome}"
