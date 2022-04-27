from dataclasses import fields
from django.forms import DateInput, DateTimeInput, ModelForm, Select, TextInput, Textarea, URLInput, widgets

from django.contrib.auth.models import User, Group
from core.models import Analysis, Mitigation, RiskAcceptance, RiskInstance
from general.models import ParentRisk, Project, ProjectsGroup, Solution

class RiskAnalysisCreateForm(ModelForm):
    class Meta:
        model = Analysis
        fields = ['project', 'auditor', 'is_draft', 'rating_matrix', 'comments']
        widgets = { # Tailwind Styles go here
            'comments': Textarea(attrs={'class': 'w-full rounded-md'}),
            'project': Select(attrs={'class': 'w-full rounded-md'}),
        }

class MeasureCreateForm(ModelForm):
    class Meta:
        model = Mitigation
        fields = '__all__'
        widgets = { # Tailwind Styles go here
            'risk_instance': Select(attrs={'class': 'w-full rounded-md'}),
            'description': Textarea(attrs={'class': 'w-full rounded-md'}),
        }

class SecurityFunctionCreateForm(ModelForm):
    class Meta:
        model = Solution
        fields = '__all__'
        widgets = { # Tailwind Styles go here
            'comments': Textarea(attrs={'class': 'w-full rounded-md'}),
        }

class ThreatCreateForm(ModelForm):
    class Meta:
        model = ParentRisk
        fields = '__all__'
        widgets = { # Tailwind Styles go here
            'title': TextInput(attrs={'class': 'w-full rounded-md'}),
        }

class UserCreateForm(ModelForm):
    class Meta:
        model = User
        fields = '__all__'
        widgets = { # Tailwind Styles go here
            'comments': Textarea(attrs={'class': 'w-full rounded-md'}),
        }

class RiskAnalysisUpdateForm(ModelForm):
    class Meta:
        model = Analysis
        fields = ['project', 'auditor', 'version', 'is_draft', 'rating_matrix', 'comments']
        widgets = { # Tailwind Styles go here
            'comments': Textarea(attrs={'class': 'w-full rounded-md'}),
        }

class RiskInstanceCreateForm(ModelForm):
    class Meta:
        model = RiskInstance
        exclude = ['analysis', 'residual_level', 'current_level']
        
        widgets = { # Tailwind Styles go here
            'analysis': Select(attrs={'class': 'w-auto rounded-md text-sm h-32'}),
            'existing_measures': Textarea(attrs={'class': 'w-full rounded-md text-sm h-32'}),
            'scenario': Textarea(attrs={'class': 'w-full rounded-md text-sm h-24'}),
            'comments': Textarea(attrs={'class': 'w-full rounded-md text-sm h-18'}),
            'parent_risk': Select(attrs={'class': 'w-full rounded-md text-sm'}),
            'current_proba': Select(attrs={'class': 'w-full rounded-md text-sm'}),
            'current_impact': Select(attrs={'class': 'w-full rounded-md text-sm'}),
            'residual_proba': Select(attrs={'class': 'w-full rounded-md text-sm'}),
            'residual_impact': Select(attrs={'class': 'w-full rounded-md text-sm'}),
            'treatment': Select(attrs={'class': 'w-full rounded-md text-sm'}),
        }

class RiskInstanceUpdateForm(ModelForm):
    class Meta:
        model = RiskInstance
        fields = '__all__'
        exclude = ['current_level', 'residual_level']
        widgets = { # Tailwind Styles go here
            'existing_measures': Textarea(attrs={'class': 'w-full rounded-md text-sm h-32'}),
            'scenario': Textarea(attrs={'class': 'w-full rounded-md text-sm h-24'}),
            'comments': Textarea(attrs={'class': 'w-full rounded-md text-sm h-18'}),
            'parent_risk': Select(attrs={'class': 'w-full rounded-md text-sm'}),
            'current_proba': Select(attrs={'class': 'w-full rounded-md text-sm'}),
            'current_impact': Select(attrs={'class': 'w-full rounded-md text-sm'}),
            'residual_proba': Select(attrs={'class': 'w-full rounded-md text-sm'}),
            'residual_impact': Select(attrs={'class': 'w-full rounded-md text-sm'}),
            'treatment': Select(attrs={'class': 'w-full rounded-md text-sm'}),
        }

class MitigationUpdateForm(ModelForm):
    class Meta:
        model = Mitigation
        exclude = ['risk_instance']
        widgets = {
            'eta': DateInput(),
            'link': URLInput(attrs={'class': 'w-full rounded-md text-sm invalid:border-pink-500 invalid:text-pink-600 focus:invalid:border-pink-500 focus:invalid:ring-pink-500'}),
        }

class ProjectsGroupUpdateForm(ModelForm):
    class Meta:
        model = ProjectsGroup
        fields = '__all__'
        widgets = { # Tailwind Styles go here
            'name': TextInput(attrs={'class': 'w-full rounded text-sm h-32 border border-gray-300'}),
            'department': TextInput(attrs={'class': 'w-full rounded text-sm h-32 border border-gray-300'}),
        }

class ProjectUpdateForm(ModelForm):
    class Meta:
        model = Project
        fields = '__all__'

class SecurityFunctionUpdateForm(ModelForm):
    class Meta:
        model = Solution
        fields = '__all__'

class ThreatUpdateForm(ModelForm):
    class Meta:
        model = ParentRisk
        fields = '__all__'

class RiskAcceptanceCreateUpdateForm(ModelForm):
    class Meta:
        model = RiskAcceptance
        fields = '__all__'
        widgets =  {
            'risk_instance': Select(attrs={'class': 'w-full rounded text-sm border border-gray-300 h-32'}),
            'validator': TextInput(attrs={'class': 'w-full rounded text-sm border border-gray-300 h-32'}),
            'type': Select(attrs={'class': 'w-full rounded text-sm border border-gray-300 h-32'}),
            'expiry_date': DateInput(attrs={'class': 'w-full rounded text-sm border border-gray-300 h-32'}),
            'comments': TextInput(attrs={'class': 'w-full rounded text-sm border border-gray-300 h-32'}),
        }

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        widgets = {
            'name': TextInput(attrs={'class': 'w-full rounded text-sm border border-gray-300 h-32'}),
            'internal_id': TextInput(attrs={'class': 'w-full rounded border border-gray-300 text-sm h-32'}),
            'parent_group': Select(attrs={'class': 'w-full rounded border border-gray-300 text-sm h-32'}),
            'lc_status': Select(attrs={'class': 'w-full rounded border border-gray-300 text-sm h-32'}),
            'summary': Textarea(attrs={'class': 'w-full rounded border border-gray-300 text-sm h-32'}),
        }