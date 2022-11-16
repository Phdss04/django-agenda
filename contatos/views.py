from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .forms import ContatoForm
from .models import Contato

# Create your views here.

def index(request):
    return render(request,"contatos/index.html")

@login_required(redirect_field_name='login')
def dashboard(request):
    contatos = Contato.objects.order_by('-id').filter(
        mostrar = True
    )
    paginator = Paginator(contatos, 7)
    page = request.GET.get('page')
    contatos = paginator.get_page(page)
    return render(request, 'contatos/dashboard.html', {
        'contatos': contatos
    })

def mostrar_contato(request, contato_id):
    contato = get_object_or_404(Contato, id=contato_id )
    if not contato.mostrar:
        messages.error(request, "Contato não encontrado")
        return redirect('dashboard')
    return render(request, 'contatos/mostrar_contato.html', {
        'contato': contato
    })
    
def busca(request):
    termo = request.GET.get('termo')  
    print(termo)
    if termo is None or not termo:
        messages.add_message(request, messages.ERROR, 'O campo de busca não deve ficar vazio')
        return redirect('index')
    else:
        campos = Concat('nome', Value(' '), 'sobrenome')
        contatos = Contato.objects.annotate(
            nome_completo = campos
        ).filter(
            Q(nome_completo__icontains = termo) | Q(id__contains = termo)
        )
        
        paginator = Paginator(contatos, 3)
        page = request.GET.get('page')
        contatos = paginator.get_page(page)
        return render(request, 'contatos/busca.html', {
            'contatos': contatos
        })

@login_required(redirect_field_name='login')
def novo_contato(request):
    if request.method == 'POST':
        form = ContatoForm(request.POST, request.FILES)
        if form.is_valid():
            contato = form.save(commit=False)
            #realizar qualquer regra de negocio nos campos antes de salvar
            contato.save()
            messages.success(request, "Contato criado com sucesso!")
            return redirect('dashboard')
        else:
            messages.error(request, "Erro ao criar contato, confira os campos e tente novamente.")
            return render(request, 'contatos/novo_contato.html')
    else:
        form = ContatoForm()
        return render(request, 'contatos/novo_contato.html', {'form': form})

@login_required(redirect_field_name='login')
def editar_contato(request, contato_id):
    contato = get_object_or_404(Contato, id=contato_id)
    form = ContatoForm(instance=contato)
    
    if request.method == 'POST':
        form = ContatoForm(request.POST, request.FILES, instance=contato)
        if form.is_valid():
            contato.save()
            messages.success(request, "Contato alterado com sucesso!")
            return redirect('dashboard')
        else:
            messages.error(request, 'Erro ao editar contato, tente novamente.')
            return render(request, 'contatos/editar_contato.html', {'form': form, 'contato' : contato})
    else: 
        return render(request, 'contatos/editar_contato.html', {'form': form, 'contato' : contato})
    
@login_required(redirect_field_name='login')
def excluir_contato(request, contato_id):
    contato = get_object_or_404(Contato, id=contato_id)
    if contato:
        contato.delete()
        print(contato)
        messages.success(request, 'Contato deletado com sucesso!')
        return redirect('dashboard')
    else:
        messages.error(request, 'Contado não encontrado.')
        return redirect('/')  