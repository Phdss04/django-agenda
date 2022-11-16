from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path("dashboard/", views.dashboard, name='dashboard'),
    path('<int:contato_id>', views.mostrar_contato, name='mostrar_contato'),
    path('busca/', views.busca, name='busca'),
    path('novo_contato/', views.novo_contato, name='novo_contato'),
    path('editar_contato/<int:contato_id>', views.editar_contato, name='editar_contato'),
    path('excluir_contato/<int:contato_id>', views.excluir_contato, name='excluir_contato'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
