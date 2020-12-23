from django import forms
from .models import VNCSession
from main.models import Organization

class VNCSessionForm(forms.ModelForm):
    class Meta:
        model = VNCSession
        fields = ('name', 'ip4_addr', 'vnc_port', 'password', 'organizations')
        widgets = {
            'name': forms.TextInput(),
            'ip4_addr': forms.TextInput(),
            'vnc_port': forms.TextInput(),
            'password': forms.PasswordInput()
        }

    organizations = forms.ModelMultipleChoiceField(queryset=Organization.objects.all())

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        if VNCSession.objects.filter(id=self.instance.id):
            self.instance.updated_by = self.request.user
        else:
            self.instance.created_by = self.request.user
        return super().save(commit=commit)


