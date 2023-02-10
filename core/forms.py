from django.forms import CheckboxInput, DateInput, DateTimeInput, EmailInput, HiddenInput, ModelForm, NullBooleanSelect, NumberInput, PasswordInput, Select, SelectMultiple, TextInput, Textarea, TimeInput, URLInput, CheckboxSelectMultiple
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm
from django import forms
from .models import *
from iam.models import RoleAssignment
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


class LoginForm(AuthenticationForm):
    username = forms.CharField(label=_("Email"), widget=forms.TextInput(attrs={'class': 'my-2 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'}))
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput(attrs={'class': 'my-2 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'}))

class ResetForm(forms.Form):
    email = forms.EmailField(label=_("Email"), widget=forms.TextInput(attrs={'class': 'my-2 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'}))


class ResetConfirmForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):  
        style = 'my-2 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'
        super(__class__, self).__init__(*args, **kwargs)
        for password in self.fields.items():
            password[1].widget.attrs['class'] = style



class RiskAnalysisCreateForm(StyledModelForm):
    class Meta:
        model = Analysis
        fields = ['project', 'name', 'description', 'auditor', 'is_draft', 'rating_matrix']
        
class RiskAnalysisCreateFormInherited(StyledModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['project'].widget.attrs['select_disabled'] = True
        
    class Meta:
        model = Analysis
        fields = ['project', 'name', 'description', 'auditor', 'is_draft', 'rating_matrix']


class RiskAnalysisUpdateForm(StyledModelForm):
    class Meta:
        model = Analysis
        fields = ['project', 'auditor', 'name', 'description', 'version', 'is_draft']


class SecurityMeasureCreateForm(StyledModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['folder'].queryset = Folder.objects.filter(content_type=Folder.ContentType.DOMAIN)
    class Meta:
        model = SecurityMeasure
        fields = '__all__'
        widgets = {
            'eta': DefaultDateInput()
        }

class SecurityMeasureCreateFormInherited(StyledModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['folder'].queryset = Folder.objects.filter(content_type=Folder.ContentType.DOMAIN)
        self.fields['folder'].widget.attrs['select_disabled'] = True

    class Meta:
        model = SecurityMeasure
        fields = '__all__'
        widgets = {
            'eta': DefaultDateInput()
        }


class SecurityMeasureUpdateForm(StyledModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['folder'].queryset = Folder.objects.filter(content_type=Folder.ContentType.DOMAIN)
    class Meta:
        model = SecurityMeasure
        fields = '__all__'
        widgets = {
            'eta': DefaultDateInput(format='%Y-%m-%d')
        }

class RiskScenarioCreateForm(StyledModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    class Meta:
        model = RiskScenario
        fields = ['analysis', 'threat', 'name', 'description']


class RiskScenarioUpdateForm(StyledModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        PROBA_CHOICES = [(-1, '--')] + list(zip(list(range(0, 10)), [x['name'] for x in self.instance.get_matrix()['probability']]))
        IMPACT_CHOICES = [(-1, '--')] + list(zip(list(range(0, 10)), [x['name'] for x in self.instance.get_matrix()['impact']]))
        self.fields['current_proba'].widget = Select(choices=PROBA_CHOICES, attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 disabled:opacity-50',
            'onchange': 'refresh();'
        })
        self.fields['current_impact'].widget = Select(choices=IMPACT_CHOICES, attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 disabled:opacity-50',
            'onchange': 'refresh();'
        })
        self.fields['residual_proba'].widget = Select(choices=PROBA_CHOICES, attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 disabled:opacity-50',
            'onchange': 'refresh();'
        })
        self.fields['residual_impact'].widget = Select(choices=IMPACT_CHOICES, attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 disabled:opacity-50',
            'onchange': 'refresh();'
        })
        self.fields['assets'].widget = CheckboxSelectMultiple(attrs={'class': 'text-sm rounded'}, choices=self.fields['assets'].choices)

    class Meta:
        model = RiskScenario
        fields = '__all__'
        exclude = ['current_level', 'residual_level']


class SecurityMeasureSelectForm(StyledModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['security_measures'].widget = CheckboxSelectMultiple(attrs={'class': 'text-sm rounded'}, choices=self.fields['security_measures'].choices)

    class Meta:
        model = RiskScenario
        fields = ['security_measures']


class RiskScenarioModalUpdateForm(StyledModelForm):
    class Meta:
        model = RiskScenario
        fields = '__all__'


class RiskAcceptanceCreateUpdateForm(StyledModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['risk_scenarios'].widget = CheckboxSelectMultiple(attrs={'class': 'text-sm rounded'}, choices=self.fields['risk_scenarios'].choices)

    class Meta:
        model = RiskAcceptance
        fields = '__all__'
        widgets = {
            'expiry_date': DefaultDateInput(format='%Y-%m-%d'),
        }
        labels = {'risk_scenario': _('Risk scenario')}


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
        self.fields['folder'].initial = Folder.objects.get(content_type=Folder.ContentType.ROOT)
        self.fields['folder'].widget.attrs['select_disabled'] = True
        

    class Meta:
        model = Threat
        fields = '__all__'
        exclude = ['is_published']


class ThreatUpdateForm(StyledModelForm):
    def __init__(self, *args, **kwargs):
        super(ThreatUpdateForm, self).__init__(*args, **kwargs)
        self.fields['folder'].queryset = Folder.objects.filter(content_type=Folder.ContentType.ROOT)
        self.fields['folder'].disabled = True
    class Meta:
        model = Threat
        fields = '__all__'
        exclude = ['is_published']


class AssetForm(StyledModelForm):
    def __init__(self, *args, **kwargs):
        super(AssetForm, self).__init__(*args, **kwargs)
        self.fields['folder'].queryset = Folder.objects.filter(content_type=Folder.ContentType.ROOT)
        self.fields['folder'].initial = Folder.objects.get(content_type=Folder.ContentType.ROOT)
        self.fields['folder'].widget.attrs['select_disabled'] = True

    class Meta:
        model = Asset
        fields = '__all__'
        exclude = ['is_published']


class SecurityFunctionCreateForm(StyledModelForm):
    def __init__(self, *args, **kwargs):
        super(SecurityFunctionCreateForm, self).__init__(*args, **kwargs)
        self.fields['folder'].queryset = Folder.objects.filter(content_type=Folder.ContentType.ROOT)
        self.fields['folder'].initial = Folder.objects.get(content_type=Folder.ContentType.ROOT)
        self.fields['folder'].widget.attrs['select_disabled'] = True

    class Meta:
        model = SecurityFunction
        fields = '__all__'
        exclude = ['is_published']


class SecurityFunctionUpdateForm(StyledModelForm):
    class Meta:
        model = SecurityFunction
        fields = '__all__'
        exclude = ['is_published']
