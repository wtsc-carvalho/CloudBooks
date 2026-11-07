from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.db import transaction
from django.db.models import Avg, Count, F, Q, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from .forms import PAGAMENTOS, CadastroForm, FinalizarForm, LoginForm, PerfilForm, PostForm
from .models import Categoria, Estante, Favorito, ItemCarrinho, ItemPedido, Livro, Pedido, Post, Usuario


def _voltar(request, *args, **kwargs):
    destino = request.POST.get("next", "")
    if destino and url_has_allowed_host_and_scheme(destino, allowed_hosts={request.get_host()}):
        return redirect(destino)
    return redirect(*args, **kwargs)


def entrada(request):
    return render(request, "entrada.html")


def home(request):
    return render(request, "catalogo.html", {
        "secao": "Gerais",
        "livros": Livro.objects.all(),
        "destaques": Livro.objects.all()[:5],
        "mais_vendidos": Livro.objects.annotate(vendidos=Sum("itens_pedido__quantidade"))
        .filter(vendidos__gt=0).order_by("-vendidos")[:6],
        "promocoes": Livro.objects.filter(promocoes__ativa=True).distinct()[:6],
        "categorias": Categoria.objects.all(),
    })


def categorias(request, pk=None):
    categoria = get_object_or_404(Categoria, pk=pk) if pk else None
    livros = Livro.objects.filter(categoria=categoria) if categoria else Livro.objects.all()
    return render(request, "catalogo.html", {
        "secao": categoria.nome if categoria else "Categorias",
        "livros": livros,
        "categorias": Categoria.objects.all(),
        "categoria_ativa": categoria,
    })


def pesquisa(request):
    termo = request.GET.get("q", "").strip()
    livros = Livro.objects.none()
    if termo:
        livros = Livro.objects.filter(
            Q(titulo__icontains=termo) | Q(autor__icontains=termo) | Q(categoria__nome__icontains=termo)
        ).distinct()
    return render(request, "catalogo.html", {
        "secao": f'Resultados para "{termo}"' if termo else "Pesquisa",
        "livros": livros,
        "categorias": Categoria.objects.all(),
    })


def livro_detalhe(request, pk):
    livro = get_object_or_404(Livro, pk=pk)
    avaliacoes = livro.posts.select_related("usuario")
    contexto = {
        "livro": livro,
        "avaliacoes": avaliacoes,
        "media_avaliacao": avaliacoes.aggregate(media=Avg("nota"))["media"],
        "estados": Estante.STATUS,
    }
    if request.user.is_authenticated:
        contexto["estante"] = Estante.objects.filter(usuario=request.user, livro=livro).first()
        contexto["favorito"] = Favorito.objects.filter(usuario=request.user, livro=livro).exists()
    return render(request, "livro.html", contexto)


@login_required
@require_POST
def alternar_favorito(request, pk):
    livro = get_object_or_404(Livro, pk=pk)
    favorito, criado = Favorito.objects.get_or_create(usuario=request.user, livro=livro)
    if not criado:
        favorito.delete()
    return _voltar(request, "livro", pk=pk)


@login_required
@require_POST
def salvar_estante(request, pk):
    livro = get_object_or_404(Livro, pk=pk)
    status = request.POST.get("status")
    if status == "remover":
        Estante.objects.filter(usuario=request.user, livro=livro).delete()
    elif status in dict(Estante.STATUS):
        Estante.objects.update_or_create(usuario=request.user, livro=livro, defaults={"status": status})
    return redirect("livro", pk=pk)


@login_required
def favoritos(request):
    colunas = [
        (nome, request.user.estantes.filter(status=codigo).select_related("livro"))
        for codigo, nome in Estante.STATUS
    ]
    return render(request, "favoritos.html", {
        "favoritos": request.user.favoritos.select_related("livro"),
        "colunas": colunas,
    })


@login_required
@require_POST
def adicionar_carrinho(request, pk):
    livro = get_object_or_404(Livro, pk=pk)
    item, _ = ItemCarrinho.objects.get_or_create(usuario=request.user, livro=livro, defaults={"quantidade": 0})
    if item.quantidade < livro.estoque:
        item.quantidade += 1
        item.save()
        messages.success(request, f'"{livro.titulo}" foi para o carrinho.')
    else:
        messages.error(request, "Este livro está esgotado ou já está no limite do estoque.")
        if item.quantidade == 0:
            item.delete()
    return _voltar(request, "carrinho")


@login_required
def carrinho(request):
    itens = list(request.user.itens_carrinho.select_related("livro"))
    bruto = sum((i.livro.preco * i.quantidade for i in itens), Decimal("0"))
    total = sum((i.subtotal for i in itens), Decimal("0"))
    return render(request, "carrinho.html", {
        "itens": itens,
        "bruto": bruto,
        "total": total,
        "desconto": bruto - total,
    })


@login_required
@require_POST
def alterar_carrinho(request, pk, acao):
    item = get_object_or_404(ItemCarrinho, pk=pk, usuario=request.user)
    if acao == "mais" and item.quantidade < item.livro.estoque:
        item.quantidade += 1
        item.save()
    elif acao == "menos":
        item.quantidade -= 1
        if item.quantidade < 1:
            item.delete()
        else:
            item.save()
    elif acao == "remover":
        item.delete()
    return redirect("carrinho")


@login_required
def finalizar(request):
    itens = list(request.user.itens_carrinho.select_related("livro"))
    if not itens:
        messages.info(request, "Seu carrinho está vazio.")
        return redirect("carrinho")
    total = sum((i.subtotal for i in itens), Decimal("0"))
    form = FinalizarForm(request.POST or None, initial={"endereco": request.user.endereco})
    if request.method == "POST" and form.is_valid():
        with transaction.atomic():
            for item in itens:
                livro = Livro.objects.select_for_update().get(pk=item.livro_id)
                if item.quantidade > livro.estoque:
                    messages.error(request, f'Estoque insuficiente para "{livro.titulo}".')
                    return redirect("carrinho")
            pedido = Pedido.objects.create(
                usuario=request.user,
                endereco=form.cleaned_data["endereco"],
                pagamento=dict(PAGAMENTOS)[form.cleaned_data["pagamento"]],
                total=total,
            )
            for item in itens:
                ItemPedido.objects.create(
                    pedido=pedido,
                    livro=item.livro,
                    quantidade=item.quantidade,
                    preco_unitario=item.livro.preco_final,
                )
                Livro.objects.filter(pk=item.livro_id).update(estoque=F("estoque") - item.quantidade)
            request.user.itens_carrinho.all().delete()
        messages.success(request, "Compra realizada com sucesso.")
        return redirect("confirmacao", pk=pedido.pk)
    return render(request, "finalizar.html", {"form": form, "total": total})


@login_required
def confirmacao(request, pk):
    pedido = get_object_or_404(Pedido.objects.prefetch_related("itens__livro"), pk=pk, usuario=request.user)
    return render(request, "confirmacao.html", {"pedido": pedido})


def cadastro(request):
    form = CadastroForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        usuario = form.save()
        auth_login(request, usuario)
        messages.success(request, "Conta criada. Bem-vindo à CloudBooks!")
        return redirect("home")
    return render(request, "cadastro.html", {"form": form})


def login_view(request):
    form = LoginForm(request.POST or None)
    erro = ""
    if request.method == "POST" and form.is_valid():
        conta = Usuario.objects.filter(email__iexact=form.cleaned_data["email"]).first()
        usuario = authenticate(
            request,
            username=conta.username if conta else None,
            password=form.cleaned_data["senha"],
        )
        if usuario:
            auth_login(request, usuario)
            return _voltar(request, "home")
        erro = "E-mail ou senha incorretos."
    return render(request, "login.html", {"form": form, "erro": erro})


def clube(request):
    agora = timezone.now()
    form = PostForm(request.POST or None)
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("login")
        if form.is_valid():
            post = form.save(commit=False)
            post.usuario = request.user
            post.save()
            messages.success(request, "Sua indicação foi publicada.")
            return redirect("clube")
    do_mes = (
        Livro.objects.annotate(
            n=Count("posts", filter=Q(posts__criado_em__year=agora.year, posts__criado_em__month=agora.month))
        )
        .filter(n__gt=0)
        .order_by("-n")
        .first()
    )
    mais_lidos = (
        Livro.objects.annotate(n=Count("estantes", filter=Q(estantes__status="lido")))
        .filter(n__gt=0)
        .order_by("-n")[:3]
    )
    return render(request, "clube.html", {
        "form": form,
        "do_mes": do_mes,
        "mais_lidos": mais_lidos,
        "posts": Post.objects.select_related("usuario", "livro")[:30],
    })


@login_required
def configuracoes(request):
    perfil = PerfilForm(instance=request.user)
    senha = PasswordChangeForm(request.user)
    if request.method == "POST" and "salvar_perfil" in request.POST:
        perfil = PerfilForm(request.POST, instance=request.user)
        if perfil.is_valid():
            perfil.save()
            messages.success(request, "Dados atualizados.")
            return redirect("configuracoes")
    if request.method == "POST" and "trocar_senha" in request.POST:
        senha = PasswordChangeForm(request.user, request.POST)
        if senha.is_valid():
            senha.save()
            update_session_auth_hash(request, senha.user)
            messages.success(request, "Senha alterada com sucesso.")
            return redirect("configuracoes")
    return render(request, "configuracoes.html", {
        "perfil": perfil,
        "senha": senha,
        "pedidos": request.user.pedidos.prefetch_related("itens__livro"),
        "avaliacoes": request.user.posts.select_related("livro"),
    })
