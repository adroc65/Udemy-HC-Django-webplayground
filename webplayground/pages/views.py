from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect
from .models import Page
from .forms import PageForm


class StaffRequiredMixin(object):
    # Esto es un Mixin para usarlo donde quiero bloquear quien administra las Páginas.
    # Se determina si el usuario es miembro del Staff para permitir crear Paginas
    # Usando Decoradores para determinar el usuario Logeado
    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kargs):
        # print(request.user)
        # if not request.user.is_staff:
        #     return redirect(reverse_lazy('admin:login'))
        return super(StaffRequiredMixin, self).dispatch(request, *args, **kargs)


# Create your views here.
class PageListView(ListView):
    model = Page


class PageDetailView(DetailView):
    model = Page


# Se puede agregar seguridad a la pagina sin el Uso de Mixin
# esto es usando el decorador de forma directa:
@method_decorator(staff_member_required, name='dispatch')  # Se usa decorador para acceder
# class PageCreate(StaffRequiredMixin, CreateView):
class PageCreate(CreateView):
    model = Page
    form_class = PageForm
    success_url = reverse_lazy('pages:pages')


@method_decorator(staff_member_required, name='dispatch')
class PageUpdate(UpdateView):
    model = Page
    form_class = PageForm
    template_name_suffix = '_update_form'

    # Se desea mostrar la pagina con los cambios echos, por esa razón debe
    # definirse el diguiente método. Se adjunta un OK a la respuesta, para
    # indicar que todo va bien.
    def get_success_url(self):
        return reverse_lazy('pages:update', args=[self.object.id]) + '?ok'


@method_decorator(staff_member_required, name='dispatch')
class PageDelete(DeleteView):
    model = Page
    success_url = reverse_lazy('pages:pages')
