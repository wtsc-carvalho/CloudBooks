from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Categoria, ItemPedido, Livro, Pedido, Post, Promocao, Usuario

admin.site.site_header = "CloudBooks · Painel administrativo"
admin.site.site_title = "CloudBooks"
admin.site.index_title = "Gestão da livraria"


class PromocaoInline(admin.TabularInline):
    model = Promocao
    extra = 0


class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0


@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    list_display = ("titulo", "autor", "categoria", "preco", "estoque")
    list_filter = ("categoria",)
    search_fields = ("titulo", "autor", "isbn")
    inlines = [PromocaoInline]


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    search_fields = ("nome",)


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ("id", "usuario", "criado_em", "total", "status")
    list_editable = ("status",)
    list_filter = ("status",)
    inlines = [ItemPedidoInline]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("livro", "usuario", "nota", "criado_em")
    list_filter = ("nota",)
    search_fields = ("texto",)


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ("username", "email", "first_name", "is_staff")
    fieldsets = UserAdmin.fieldsets + (
        ("Dados da livraria", {"fields": ("telefone", "cpf", "data_nascimento", "cep", "endereco")}),
    )
