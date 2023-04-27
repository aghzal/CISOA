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

from core.views import BaseContextMixin
import json

class LibraryListView(BaseContextMixin, FormView):
    template_name = 'library/library_list.html'
    form_class = UploadFileForm
    success_url = reverse_lazy('library-list')

    def get_queryset(self):
        qs = get_available_libraries()
        for lib in qs:
            lib['threats'] = len([x for x in lib['objects'] if x['type'] == 'threat'])
            lib['matrices'] = len([x for x in lib['objects'] if x['type'] == 'matrix'])
            lib['security_functions'] = len([x for x in lib['objects'] if x['type'] == 'security_function'])
            lib['objects'].clear()
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['libraries'] = self.get_queryset()
        context['matrix_import'] = RoleAssignment.is_access_allowed(self.request.user, Permission.objects.get(codename="add_riskmatrix"), Folder.get_root_folder())
        context['threat_import'] = RoleAssignment.is_access_allowed(self.request.user, Permission.objects.get(codename="add_threat"), Folder.get_root_folder())
        context['securityfunction_import'] = RoleAssignment.is_access_allowed(self.request.user, Permission.objects.get(codename="add_securityfunction"), Folder.get_root_folder())
        context['form'] = UploadFileForm()
        return context

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file')
        for f in files:
            try:
                validate_file_extension(f)
                library = json.load(f)
                import_library_view(request, library)
                return self.form_valid(form)
            except ValidationError as e:
                messages.error(request, _("Failed to import file: {}. {}").format(f.name, e.message % e.params))
                return self.form_invalid(form)


class LibraryDetailView(BaseContextMixin, TemplateView):
    template_name = 'library/library_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        library = get_library(kwargs['library'])
        context['library'] = library
        context['types'] = self.get_object_types(library)
        matrices_list = []
        for matrices in self.get_matrices(library):
            fields = matrices['fields']
            matrices_list.append(RiskMatrix(name=fields['name'],
                                                    description=fields['description'],
                                                    json_definition=json.dumps(fields)))
        context['matrices'] = matrices_list
        object_type = self.get_object_types(library).pop().replace("_", "")
        if object_type == "matrix":
            object_type = "riskmatrix"
        context['can_import'] = RoleAssignment.is_access_allowed(
                                self.request.user,
                                Permission.objects.get(codename="add_"+object_type),
                                Folder.get_root_folder())
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
        messages.error(request, _("Failed to import library: {}").format(library_name))
    return redirect("library-list")