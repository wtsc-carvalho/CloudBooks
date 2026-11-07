from decimal import Decimal

from django.core.management.base import BaseCommand

from loja.models import Categoria, Estante, Livro, Post, Promocao, Usuario

LIVROS = [
    ("Dom Casmurro", "Machado de Assis", "Romance", "978-85-0000-001-1", 1899, 256,
     "Bentinho revisita a juventude e a dúvida que mudou sua vida.", "29.90", 12),
    ("O Hobbit", "J. R. R. Tolkien", "Fantasia", "978-85-0000-002-8", 1937, 366,
     "Bilbo Bolseiro é arrancado do conforto de casa rumo a uma grande aventura.", "49.90", 8),
    ("Drácula", "Bram Stoker", "Terror", "978-85-0000-003-5", 1897, 418,
     "Um advogado inglês viaja à Transilvânia e descobre um segredo sombrio.", "39.90", 6),
    ("Neuromancer", "William Gibson", "Ficção científica", "978-85-0000-004-2", 1984, 280,
     "Um hacker decadente recebe uma última chance de voltar ao ciberespaço.", "44.90", 5),
    ("O Silêncio dos Inocentes", "Thomas Harris", "Suspense", "978-85-0000-005-9", 1988, 376,
     "Uma agente do FBI busca ajuda de um psiquiatra preso para caçar um assassino.", "42.90", 7),
    ("Hábitos Atômicos", "James Clear", "Desenvolvimento pessoal", "978-85-0000-006-6", 2018, 320,
     "Como pequenas mudanças diárias geram resultados duradouros.", "59.90", 15),
    ("Fahrenheit 451", "Ray Bradbury", "Ficção científica", "978-85-0000-007-3", 1953, 240,
     "Um bombeiro que queima livros começa a questionar o próprio ofício.", "34.90", 9),
    ("Os Miseráveis", "Victor Hugo", "Drama", "978-85-0000-008-0", 1862, 1463,
     "A saga de Jean Valjean em uma França marcada pela desigualdade.", "89.90", 4),
    ("A Ilha do Tesouro", "Robert Louis Stevenson", "Aventura", "978-85-0000-009-7", 1883, 288,
     "Um mapa, um navio pirata e a busca por um tesouro escondido.", "27.90", 10),
    ("Coraline", "Neil Gaiman", "Fantasia", "978-85-0000-010-3", 2002, 192,
     "Uma menina descobre uma casa paralela onde tudo parece perfeito demais.", "31.90", 11),
]

INDICACOES = [
    ("Dom Casmurro", 5, "Um clássico que faz a gente duvidar de cada página."),
    ("O Hobbit", 5, "Aventura leve e cheia de charme. Impossível largar."),
    ("Hábitos Atômicos", 4, "Ideias práticas que dá para aplicar na semana seguinte."),
]


class Command(BaseCommand):
    help = "Preenche o banco com categorias, livros, usuários, promoções e indicações de exemplo."

    def handle(self, *args, **options):
        for titulo, autor, categoria, isbn, ano, paginas, descricao, preco, estoque in LIVROS:
            Livro.objects.update_or_create(
                isbn=isbn,
                defaults={
                    "titulo": titulo,
                    "autor": autor,
                    "categoria": Categoria.objects.get_or_create(nome=categoria)[0],
                    "ano_publicacao": ano,
                    "num_paginas": paginas,
                    "descricao": descricao,
                    "preco": Decimal(preco),
                    "estoque": estoque,
                },
            )

        if not Usuario.objects.filter(username="admin").exists():
            Usuario.objects.create_superuser(
                "admin", "admin@cloudbooks.com", "admin123", first_name="Administradora"
            )

        leitor, criado = Usuario.objects.get_or_create(
            username="leitor",
            defaults={
                "email": "leitor@cloudbooks.com",
                "first_name": "Leitora Demo",
                "endereco": "Rua das Estrelas, 100",
            },
        )
        if criado:
            leitor.set_password("leitor123")
            leitor.save()

        for livro in Livro.objects.all()[:2]:
            Promocao.objects.get_or_create(livro=livro, defaults={"percentual": 15})

        if not Post.objects.exists():
            for titulo, nota, texto in INDICACOES:
                livro = Livro.objects.get(titulo=titulo)
                Post.objects.create(usuario=leitor, livro=livro, nota=nota, texto=texto)
                Estante.objects.update_or_create(usuario=leitor, livro=livro, defaults={"status": "lido"})

        self.stdout.write(self.style.SUCCESS(
            "Dados de exemplo criados. Painel: admin / admin123 · Cliente: leitor / leitor123"
        ))
