from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth import authenticate
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.
def login(request):
    if request.method != 'POST':
        return render(request, 'accounts/login.html')
    
    print(request.POST)
    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')
    user = auth.authenticate(request, username=usuario, password=senha)
    if user is not None:
        auth.login(request, user)
        messages.success(request, 'Logado com sucesso')
        return redirect('dashboard')
    else:
        messages.error(request, 'Usuário ou senha inválidos')
        print(usuario, senha)
        return render(request, 'accounts/login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

def register(request):
    if request.method != 'POST':
        return render(request, 'accounts/register.html')
    nome = request.POST.get('nome')
    sobrenome = request.POST.get('sobrenome')
    email = request.POST.get('email')
    usuario = request.POST.get('usuario')
    senha1 = request.POST.get('senha1')
    senha2 = request.POST.get('senha2')
    
    if not nome or not sobrenome or not email or not usuario or not senha1 or not senha2:
        messages.error(request, "Nenhum campo pode estar vazio")
        return render(request, 'accounts/register.html')
    try:
        validate_email(email)
    except:
        messages.error(request, "Email inválido")
        return render(request, 'accounts/register.html')
    
    if senha1 != senha2:
            messages.error(request, "Senhas diferentes")
            return render(request, 'accounts/register.html')
    
    if not len(senha1) > 5:
        messages.error(request, "Senha muito curta")
        return render(request, 'accounts/register.html')
    
    if User.objects.filter(username=usuario).exists():
        messages.error(request, "Este usuário já existe")
        return render(request, 'accounts/register.html')
    
    if User.objects.filter(email=email).exists():
        messages.error(request, "Este email já existe")
        return render(request, 'accounts/register.html')

    user = User.objects.create_user(username=usuario, email=email, password=senha1, first_name=nome, last_name=sobrenome)
    user.save()
    messages.success(request, "Usuário cadastrado com sucesso! Realize o login.")
    return redirect('login')
    
@login_required(redirect_field_name='login')
def dashboard(request):
    return render(request, 'accounts/dashboard.html')