from django.urls import path
from django.contrib.auth.decorators import login_required, permission_required
from .views import PageListView, PageDetailView, PageCreate, PageUpdate, PageDelete


pages_patterns = ([
    path('', PageListView.as_view(), name='pages'),
    path('<int:pk>/<slug:slug>/', PageDetailView.as_view(), name='page'),
    path('create/', PageCreate.as_view(), name='create'),
    # Se comenta la línea superior para pedir que el acceso a Crear paginas sea solo para usuarios Logeados.
    # path('create/', login_required(PageCreate.as_view(template_name='create'))),
    path('update/<int:pk>/', PageUpdate.as_view(), name='update'),
    path('delete/<int:pk>/', PageDelete.as_view(), name='delete'),
], 'pages')
