from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

urlpatterns = [
    path("", views.entrada, name="entrada"),
    path("home/", views.home, name="home"),
    path("pesquisa/", views.pesquisa, name="pesquisa"),
    path("categorias/", views.categorias, name="categorias"),
    path("categorias/<int:pk>/", views.categorias, name="categoria"),
    path("livro/<int:pk>/", views.livro_detalhe, name="livro"),
    path("livro/<int:pk>/carrinho/", views.adicionar_carrinho, name="adicionar_carrinho"),
    path("livro/<int:pk>/favorito/", views.alternar_favorito, name="alternar_favorito"),
    path("livro/<int:pk>/estante/", views.salvar_estante, name="salvar_estante"),
    path("cadastro/", views.cadastro, name="cadastro"),
    path("login/", views.login_view, name="login"),
    path("sair/", LogoutView.as_view(next_page="entrada"), name="sair"),
    path("carrinho/", views.carrinho, name="carrinho"),
    path("carrinho/<int:pk>/<str:acao>/", views.alterar_carrinho, name="alterar_carrinho"),
    path("clube/", views.clube, name="clube"),
    path("favoritos/", views.favoritos, name="favoritos"),
    path("finalizar/", views.finalizar, name="finalizar"),
    path("pedido/<int:pk>/", views.confirmacao, name="confirmacao"),
    path("conta/", views.configuracoes, name="configuracoes"),
]
