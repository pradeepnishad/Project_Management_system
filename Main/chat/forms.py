from django import forms
from .models import Message


class MessageForm(forms.ModelForm):

    use_ai = forms.BooleanField(
        required=False,
        initial=False,
        label="Improve grammar using AI"
    )

    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Type your message...'
            })
        }