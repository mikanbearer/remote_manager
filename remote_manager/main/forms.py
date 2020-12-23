from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from .models import CustomUser, Organization

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'organization', 'is_staff', 'is_active')
        widgets = {
            'username': forms.TextInput(),
            'is_staff': forms.CheckboxInput(),
            'is_active': forms.CheckboxInput()
        }

    organization = forms.ModelChoiceField(queryset=Organization.objects.all())

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        if CustomUser.objects.filter(id=self.instance.id):
            self.instance.updated_by = self.request.user
        else:
            self.instance.created_by = self.request.user
        return super().save(commit=commit)


class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ('name',)
        widgets = {
            'name': forms.TextInput()
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        if Organization.objects.filter(id=self.instance.id):
            self.instance.updated_by = self.request.user
        else:
            self.instance.created_by = self.request.user
        return super().save(commit=commit)
