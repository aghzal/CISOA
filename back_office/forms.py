from typing import Any, Dict
from django.forms import CheckboxInput, DateInput, DateTimeInput, EmailInput, HiddenInput, ModelForm, NullBooleanSelect, NumberInput, PasswordInput, Select, SelectMultiple, TextInput, Textarea, TimeInput, URLInput
from .models import *
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model


User = get_user_model()

class DefaultDateInput(DateInput):
    input_type = 'date'

class StyledModelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(__class__, self).__init__(*args, **kwargs)
        text_inputs = (TextInput, NumberInput, EmailInput, URLInput, PasswordInput, HiddenInput, DefaultDateInput, DateInput, DateTimeInput, TimeInput)
        select_inputs = (Select, SelectMultiple, NullBooleanSelect)
        for fname, f in self.fields.items():
            input_type = f.widget.__class__
            if self.Meta.model:
                model_name = str(self.Meta.model).split('.')[-1].strip("'>").lower()
            if input_type in text_inputs:
                f.widget.attrs['id'] = f'id_{model_name}_{fname}' if model_name else f'id_{fname}'
                f.widget.attrs['class'] = 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5'
            if input_type in select_inputs:
                f.widget.attrs['id'] = f'id_{model_name}_{fname}'
                f.widget.attrs['class'] = 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 disabled:opacity-50'
            if input_type == Textarea:
                f.widget.attrs['class'] = 'block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500'
            if input_type == CheckboxInput:
                f.widget.attrs['id'] = f'id_{model_name}_{fname}'
                f.widget.attrs['class'] = 'w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500'
            if input_type == DefaultDateInput:
                f.widget.attrs['id'] = f'id_{model_name}_{fname}'
                f.widget.attrs['class'] = 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5'
                

class ProjectForm(StyledModelForm):
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.fields['folder'].queryset = Folder.objects.filter(content_type=Folder.ContentType.DOMAIN)

    class Meta:
        model = Project
        fields = '__all__'
        labels = {'folder': _('Domain')}

class ProjectFormInherited(StyledModelForm):
    def __init__(self, *args, **kwargs):
        super(ProjectFormInherited, self).__init__(*args, **kwargs)
        self.fields['folder'].queryset = Folder.objects.filter(content_type=Folder.ContentType.DOMAIN)
        self.fields['folder'].widget.attrs['select_disabled'] = True

    class Meta:
        model = Project
        fields = '__all__'
        labels = {'folder': _('Domain')}

class ProjectUpdateForm(StyledModelForm):

    class Meta:
        model = Project
        fields = '__all__'


class ThreatCreateForm(StyledModelForm):
    def __init__(self, *args, **kwargs):
        super(ThreatCreateForm, self).__init__(*args, **kwargs)
        self.fields['folder'].queryset = Folder.objects.filter(content_type=Folder.ContentType.ROOT)
        self.fields['folder'].initial = Folder.objects.get(content_type=Folder.ContentType.ROOT).id
        

    class Meta:
        model = Threat
        fields = '__all__'
        exclude = ['is_published']


class ThreatUpdateForm(StyledModelForm):

    class Meta:
        model = Threat
        fields = '__all__'
        exclude = ['is_published']


class AssetForm(StyledModelForm):
    def __init__(self, *args, **kwargs):
        super(AssetForm, self).__init__(*args, **kwargs)
        self.fields['folder'].queryset = Folder.objects.filter(content_type=Folder.ContentType.ROOT)
        self.fields['folder'].initial = Folder.objects.get(content_type=Folder.ContentType.ROOT).id

    def clean(self) -> Optional[Dict[str, Any]]:
        super().clean()
        content_type = self.cleaned_data.get('content_type')
        parent_asset = self.cleaned_data.get('parent_asset')
        if content_type == 'SP' and parent_asset is None:
            self.add_error('parent_asset', 'A support asset must have a parent asset.')
        if content_type == 'PR' and parent_asset is not None:
            self.add_error('parent_asset', 'A primary asset cannot have a parent asset.')
        return self.cleaned_data

    class Meta:
        model = Asset
        fields = '__all__'
        exclude = ['is_published']


class SecurityFunctionCreateForm(StyledModelForm):
    def __init__(self, *args, **kwargs):
        super(SecurityFunctionCreateForm, self).__init__(*args, **kwargs)
        self.fields['folder'].queryset = Folder.objects.filter(content_type=Folder.ContentType.ROOT)
        self.fields['folder'].initial = Folder.objects.get(content_type=Folder.ContentType.ROOT).id

    class Meta:
        model = SecurityFunction
        fields = '__all__'
        exclude = ['is_published']


class SecurityFunctionUpdateForm(StyledModelForm):
    class Meta:
        model = SecurityFunction
        fields = '__all__'
        exclude = ['is_published']
