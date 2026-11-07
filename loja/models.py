from decimal import Decimal

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Usuario(AbstractUser):
    telefone = models.CharField(max_length=20, blank=True)
    cpf = models.CharField("CPF", max_length=14, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)
    cep = models.CharField("CEP", max_length=9, blank=True)
    endereco = models.CharField("endereço", max_length=200, blank=True)


class Categoria(models.Model):
    nome = models.CharField(max_length=80, unique=True)

    class Meta:
        ordering = ["nome"]
        verbose_name_plural = "categorias"

    def __str__(self):
        return self.nome


class Livro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=150)
    categoria = models.ForeignKey(
        Categoria, on_delete=models.PROTECT, related_name="livros"
    )
    isbn = models.CharField("ISBN", max_length=17, unique=True)
    ano_publicacao = models.PositiveIntegerField("ano de publicação")
    num_paginas = models.PositiveIntegerField("número de páginas")
    idioma = models.CharField(max_length=40, default="Português")
    descricao = models.TextField("descrição ou sinopse")
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    estoque = models.PositiveIntegerField("quantidade em estoque", default=0)
    capa = models.ImageField("capa", upload_to="capas/", blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-criado_em"]

    def __str__(self):
        return self.titulo

    @property
    def classe_capa(self):
        return f"capa-{self.pk % 5}"

    @property
    def preco_final(self):
        promocao = self.promocoes.filter(ativa=True).order_by("-percentual").first()
        if promocao is None:
            return self.preco
        return (self.preco * (100 - promocao.percentual) / 100).quantize(
            Decimal("0.01")
        )


class Promocao(models.Model):
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE, related_name="promocoes")
    percentual = models.PositiveSmallIntegerField(
        "desconto (%)", validators=[MinValueValidator(1), MaxValueValidator(90)]
    )
    ativa = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.percentual}% em {self.livro}"


class ItemCarrinho(models.Model):
    usuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name="itens_carrinho"
    )
    livro = models.ForeignKey(
        Livro, on_delete=models.CASCADE, related_name="itens_carrinho"
    )
    quantidade = models.PositiveIntegerField(default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["usuario", "livro"], name="item_unico_no_carrinho"
            ),
        ]

    @property
    def subtotal(self):
        return self.livro.preco_final * self.quantidade


class Pedido(models.Model):
    STATUS = [
        ("pendente", "Pendente"),
        ("pago", "Pago"),
        ("enviado", "Enviado"),
        ("entregue", "Entregue"),
        ("cancelado", "Cancelado"),
    ]

    usuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name="pedidos"
    )
    criado_em = models.DateTimeField(auto_now_add=True)
    endereco = models.CharField("endereço de entrega", max_length=200)
    pagamento = models.CharField(max_length=40)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS, default="pago")

    class Meta:
        ordering = ["-criado_em"]


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="itens")
    livro = models.ForeignKey(
        Livro, on_delete=models.PROTECT, related_name="itens_pedido"
    )
    quantidade = models.PositiveIntegerField()
    preco_unitario = models.DecimalField(max_digits=8, decimal_places=2)


class Favorito(models.Model):
    usuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name="favoritos"
    )
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE, related_name="favoritos")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["usuario", "livro"], name="favorito_unico"),
        ]


class Estante(models.Model):
    STATUS = [
        ("desejo_ler", "Desejo ler"),
        ("lendo", "Lendo"),
        ("lido", "Já lidos"),
    ]

    usuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name="estantes"
    )
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE, related_name="estantes")
    status = models.CharField(max_length=20, choices=STATUS)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["usuario", "livro"], name="estante_unica"),
        ]


class Post(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="posts")
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE, related_name="posts")
    texto = models.CharField(max_length=500)
    nota = models.PositiveSmallIntegerField(choices=[(n, str(n)) for n in range(1, 6)])
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-criado_em"]
