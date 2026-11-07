from django import forms

from .models import Post, Usuario

PAGAMENTOS = [("pix", "Pix"), ("cartao", "Cartão de crédito"), ("boleto", "Boleto")]

ROTULOS = {
    "first_name": "Nome completo",
    "username": "Nome de usuário",
    "email": "E-mail",
    "telefone": "Telefone",
    "data_nascimento": "Data de nascimento",
    "cpf": "CPF",
    "cep": "CEP",
    "endereco": "Endereço",
}


class BaseUsuarioForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for campo in self.fields.values():
            campo.required = True

    def clean_email(self):
        email = self.cleaned_data["email"]
        if Usuario.objects.filter(email__iexact=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Este e-mail já está cadastrado.")
        return email


class CadastroForm(BaseUsuarioForm):
    senha = forms.CharField(label="Senha", min_length=6, widget=forms.PasswordInput)
    confirmar_senha = forms.CharField(label="Confirmar senha", widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ["first_name", "username", "email", "telefone", "data_nascimento", "cpf", "cep", "endereco"]
        labels = ROTULOS
        widgets = {"data_nascimento": forms.DateInput(attrs={"type": "date"})}

    def clean(self):
        dados = super().clean()
        if dados.get("senha") and dados.get("senha") != dados.get("confirmar_senha"):
            self.add_error("confirmar_senha", "As senhas não coincidem.")
        return dados

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.set_password(self.cleaned_data["senha"])
        if commit:
            usuario.save()
            self.save_m2m()
        return usuario


class PerfilForm(BaseUsuarioForm):
    class Meta:
        model = Usuario
        fields = ["first_name", "email", "telefone", "cep", "endereco"]
        labels = ROTULOS


class LoginForm(forms.Form):
    email = forms.EmailField(label="E-mail")
    senha = forms.CharField(label="Senha", widget=forms.PasswordInput)


class FinalizarForm(forms.Form):
    endereco = forms.CharField(label="Endereço de entrega", max_length=200)
    pagamento = forms.ChoiceField(
        label="Forma de pagamento (simulada)", choices=PAGAMENTOS, widget=forms.RadioSelect
    )


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["livro", "texto", "nota"]
        labels = {"livro": "Livro", "texto": "O que você achou?", "nota": "Nota"}
        widgets = {"texto": forms.Textarea(attrs={"rows": 3})}
