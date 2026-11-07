# CloudBooks — Livraria virtual

Projeto de livraria virtual desenvolvido com **Python, Django, HTML, CSS, JavaScript e SQLite**.

## Requisitos

- Python 3.10 ou superior
- VS Code (recomendado)

## Como rodar o projeto

1. Extraia o arquivo `CloudBooks.zip` e abra a pasta `CloudBooks` no VS Code.
2. Abra o terminal dentro da pasta `CloudBooks` (a pasta onde está o arquivo `manage.py`).
3. Crie e ative o ambiente virtual:
   - Windows: `python -m venv venv` e depois `venv\Scripts\activate`
   - Linux/macOS: `python3 -m venv venv` && `source venv/bin/activate`
4. Instale as dependências:
   `pip install -r requirements.txt`
5. Crie as tabelas do banco de dados:
   `python manage.py makemigrations loja`
   `python manage.py migrate`
6. Carregue os dados de exemplo (recomendado):
   `python manage.py popular_loja`
7. Inicie o servidor:
   `python manage.py runserver`
8. Abra no navegador: http://127.0.0.1:8000/

## Contas de teste

| Perfil | Usuário | Senha | Acesso |
| --- | --- | --- | --- |
| Painel administrativo | admin | admin123 | http://127.0.0.1:8000/admin/ |
| Cliente | leitor | leitor123 | Login em http://127.0.0.1:8000/login/ |

Também é possível criar uma conta nova pela tela de cadastro.

## Telas do projeto

| Nº | Tela | Endereço |
| --- | --- | --- |
| 1 | Entrada (Explorar, Login e Cadastro) | `/` |
| 2 | Home (carrossel de destaques e livros gerais) | `/home/` |
| 3 | Cadastro (10 campos) | `/cadastro/` |
| 4 | Login (e-mail e senha) | `/login/` |
| 5 | Carrinho (quantidades, descontos e total) | `/carrinho/` |
| 6 | Clube de leitura (feed tipo TikTok) | `/clube/` |
| 7 | Painel administrativo | `/admin/` |
| 8 | Minha conta e Configurações (perfil, senha e pedidos) | `/conta/` |
| 9 | Detalhes do livro (avaliações, favoritos e estante) | `/livro/<id>/` |
| 10 | Categorias | `/categorias/` |
| 11 | Pesquisa (título, autor ou categoria) | `/pesquisa/?q=termo` |
| 12 | Favoritos e Minha estante | `/favoritos/` |
| 13 | Finalização da compra | `/finalizar/` |
| 14 | Confirmação do pedido | `/pedido/<id>/` |

## Regras de funcionamento

- **Compra simulada:** nenhuma cobrança real é feita. O pedido é registrado, o estoque é baixado e a forma de pagamento (Pix, cartão ou boleto) é apenas informativa.
- **Livro do mês:** é o livro com mais indicações no Clube de leitura no mês atual.
- **Mais lidos:** são os livros marcados como "Já lidos" nas estantes dos usuários.
- **Promoções:** cadastradas no painel administrativo, dentro de cada livro.
- **Capas:** quando nenhuma imagem é enviada, o livro aparece com uma capa colorida e o título.
- **Upload de capa:** exige a biblioteca Pillow, que já está em `requirements.txt`.

## Como zerar o banco de dados

Apague o arquivo `db.sqlite3`, apague os arquivos da pasta `loja/migrations/` exceto `__init__.py`, e refaça os passos 5 e 6.

## Estrutura principal

- `cloudbooks/`: configurações do projeto (settings, urls).
- `loja/`: modelos, formulários, views, rotas, painel administrativo e comando de dados de exemplo.
- `templates/`: páginas HTML.
- `static/`: CSS e JavaScript.
