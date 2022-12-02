from typing import Optional
from core.models import RiskMatrix, Threat
from iam.models import RoleAssignment

from .utils import *
from .forms import *

from django.views.generic import TemplateView, ListView, FormView
from django.views import View
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _

class LibraryListView(FormView):
    template_name = 'library/library_list.html'
    form_class = UploadFileForm
    success_url = reverse_lazy('library-list')

    def get_queryset(self):
        qs = get_available_libraries()
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['libraries'] = self.get_queryset()
        context['change_usergroup'] = RoleAssignment.has_permission(self.request.user, "change_usergroup")
        context['view_user'] = RoleAssignment.has_permission(self.request.user, "view_user")
        context['form'] = UploadFileForm()
        return context

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file')
        if form.is_valid():
            for f in files:
                library = json.load(f)
                import_library_view(request, library)
            return self.form_valid(form)
        else:
            messages.error(request, _('Invalid form.'))
            return self.form_invalid(form)


class LibraryDetailView(TemplateView):
    template_name = 'library/library_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        library = get_library(kwargs['library'])
        context['change_usergroup'] = RoleAssignment.has_permission(self.request.user, "change_usergroup")
        context['view_user'] = RoleAssignment.has_permission(self.request.user, "view_user")
        context['library'] = library
        context['types'] = self.get_object_types(library)
        context['matrices'] = self.get_matrices(library)
        context['crumbs'] = {'library-list': _('Libraries')}
        return context

    def get_object_types(self, library):
        types = set()
        for obj in library.get('objects'):
            types.add(obj['type'])
        return types

    def get_matrices(self, library):
        matrices = []
        for obj in library.get('objects'):
            if obj['type'] == 'matrix':
                matrices.append(obj)
        return matrices

def import_default_library(request, library_name):
    try:
        library = get_library(library_name)
        import_library_view(request, library)
    except:
        return redirect("library-list")
    return redirect("library-list")