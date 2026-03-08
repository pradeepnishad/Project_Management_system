from django import forms
from django.contrib.auth import get_user_model
from .models import Project
from accounts.models import AssociateProfile

User = get_user_model()


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'price_bid', 'complexity', 'urgency']





class AssignmentForm(forms.ModelForm):
    manager = forms.ModelChoiceField(
        queryset=User.objects.filter(role='manager'),
        required=True
    )

    associates = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(role='associate'),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Project
        fields = ['manager', 'associates']


class ManagerAssignAssociatesForm(forms.ModelForm):

    associates = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(role="associate"),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Project
        fields = ["associates"]