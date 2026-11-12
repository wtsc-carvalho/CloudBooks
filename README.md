# 📚 CloudBooks — Livraria Virtual

Um sistema completo de livraria virtual desenvolvido para oferecer uma excelente experiência de usuário, com recursos de e-commerce e interação social. O visual do projeto proporciona uma imersão única, adotando uma temática mágica com céus estrelados, nuvens e castelos literários flutuantes.

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-323330?style=for-the-badge&logo=javascript&logoColor=F7DF1E)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)

---

## 🎨 Identidade Visual e Paleta de Cores

O design UI/UX do CloudBooks foi construído sobre uma paleta "Dark Mode" elegante, que combina tons profundos de roxo e azul noturno com contrastes em dourado, remetendo ao universo da fantasia e magia.

**Cores Principais (Fundos e Temas):**
* `#0B0B1A` — Fundo Principal
* `#1A1033` — Fundo Secundário
* `#3A1B6B` — Roxo Principal
* `#D9B36F` — Dourado Principal (Destaques)

**Cores de Texto e UI:**
* `#FAF8F6` — Texto Principal
* `#E5D6B8` — Texto Secundário
* `#1F1F2E` — Painéis e Cards

**Cores de Estado:**
* `#9B6BFF` — Hover
* `#B67CFF` — Ativo
* `#FF6B8B` — Erro / Alerta

---

## 📸 Telas da Aplicação

A interface foi pensada para ser intuitiva e visualmente deslumbrante. Abaixo estão os destaques da navegação:

1. **Página Inicial (Home):** Apresenta um carrossel de destaques ("Os livros mais bem avaliados"), uma barra de pesquisa centralizada e botões de acesso rápido às categorias (Romance, Fantasia, Suspense, etc.).
2. **Carrinho de Compras:** Interface limpa mostrando os itens selecionados, controles de quantidade, cálculo automático de subtotais e opções de finalização de compra rápida (ex: Google Pay).
3. **Área do Usuário (Login, Cadastro e Configurações):** Formulários integrados e um painel de "Configurações" completo onde o usuário pode alternar entre temas (Claro/Escuro/Automático), gerenciar notificações e privacidade.

---

## 📋 Pré-requisitos

Antes de começar, você precisará ter instalado em sua máquina:
* **Python 3.10** ou superior
* Editor de código recomendado: **[VS Code](https://code.visualstudio.com/)**

---

## 🚀 Como rodar o projeto localmente

Siga o passo a passo abaixo para configurar o ambiente e executar a aplicação:

**1. Extraia e abra o projeto**
Descompacte o arquivo `CloudBooks.zip` e abra a pasta `CloudBooks` no seu editor (VS Code).

**2. Abra o terminal**
Certifique-se de estar no diretório raiz do projeto (onde está localizado o arquivo `manage.py`).

**3. Crie e ative o ambiente virtual**
* 🪟 **Windows:**
  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```
* 🍎/🐧 **Linux ou macOS:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

**4. Instale as dependências**
```bash
pip install -r requirements.txt
```

**5. Configure o banco de dados**
Crie as tabelas executando as migrações:
```bash
python manage.py makemigrations loja
python manage.py migrate
```

**6. Carregue os dados de exemplo (Recomendado)**
Popule a loja com livros e categorias para testar as funcionalidades:
```bash
python manage.py popular_loja
```

**7. Inicie o servidor**
```bash
python manage.py runserver
```
🌐 Acesse no navegador: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 🔐 Contas de Teste

Utilize as credenciais abaixo para explorar os diferentes perfis da plataforma:

| Perfil | Usuário | Senha | Acesso Rápido | 
| :--- | :--- | :--- | :--- | 
| 🛡️ **Administrador** | `admin` | `admin123` | [Painel Admin](http://127.0.0.1:8000/admin/) | 
| 👤 **Cliente** | `leitor` | `leitor123` | [Página de Login](http://127.0.0.1:8000/login/) | 

> 💡 *Dica: Você também pode criar uma nova conta testando o fluxo de cadastro na página inicial da aplicação.*

---

## 🗺️ Mapa de Telas

Abaixo estão as principais rotas disponíveis na aplicação:

| Nº | Tela | Rota | 
| :---: | :--- | :--- | 
| 1 | Entrada (Explorar, Login e Cadastro) | `/` | 
| 2 | Home (Carrossel de destaques e livros gerais) | `/home/` | 
| 3 | Cadastro | `/cadastro/` | 
| 4 | Login | `/login/` | 
| 5 | Carrinho (Quantidades, descontos e total) | `/carrinho/` | 
| 6 | Clube de Leitura (Feed interativo tipo TikTok) | `/clube/` | 
| 7 | Painel Administrativo | `/admin/` | 
| 8 | Minha Conta (Perfil, senha, pedidos e configs) | `/conta/` | 
| 9 | Detalhes do Livro (Avaliações e favoritos) | `/livro/<id>/` | 
| 10 | Categorias | `/categorias/` | 
| 11 | Pesquisa (Título, autor ou categoria) | `/pesquisa/?q=termo` | 
| 12 | Favoritos e Minha Estante | `/favoritos/` | 
| 13 | Finalização da Compra | `/finalizar/` | 
| 14 | Confirmação do Pedido | `/pedido/<id>/` | 

---

## ⚙️ Regras de Negócio e Funcionamento

* 🛒 **Compra Simulada:** O sistema não realiza cobranças reais. O fluxo apenas registra o pedido, deduz o estoque e exibe a forma de pagamento (Pix, Cartão ou Boleto) em caráter informativo.
* 🏆 **Livro do Mês:** O título com maior número de indicações no "Clube de Leitura" durante o mês atual ganha este destaque.
* 📈 **Mais Lidos:** Lista gerada dinamicamente com base nos livros marcados como "Já lidos" nas estantes dos clientes.
* 🏷️ **Promoções:** Gerenciadas de forma individual diretamente pelo Painel Administrativo, dentro do cadastro de cada livro.
* 🖼️ **Gerenciamento de Capas:**
  * Se nenhuma imagem for enviada, o sistema gera automaticamente uma capa colorida com o título do livro.
  * O upload de imagens customizadas utiliza a biblioteca `Pillow` (já exigida no `requirements.txt`).

---

## 🧹 Como zerar o banco de dados

Caso precise limpar todas as informações e recomeçar do zero:
1. Apague o arquivo `db.sqlite3` na raiz do projeto.
2. Apague todos os arquivos dentro da pasta `loja/migrations/`, **EXCETO** o arquivo `__init__.py`.
3. Repita os **passos 5 e 6** do guia de instalação acima.

---

## 📁 Estrutura Principal de Diretórios

```text
📦 CloudBooks
 ┣ 📂 cloudbooks/     # Configurações globais do projeto (settings, urls)
 ┣ 📂 loja/           # App principal: models, forms, views, rotas e admin
 ┣ 📂 templates/      # Arquivos HTML da interface
 ┣ 📂 static/         # Arquivos estáticos (CSS, JavaScript, Imagens)
 ┗ 📜 manage.py       # Gerenciador de execução do Django
```
