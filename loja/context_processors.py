def carrinho(request):
    if request.user.is_authenticated:
        return {"qtd_carrinho": sum(request.user.itens_carrinho.values_list("quantidade", flat=True))}
    return {"qtd_carrinho": 0}
