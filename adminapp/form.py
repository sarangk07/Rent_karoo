from django import forms
from home.models import Cars


class CarUpdateForm(forms.ModelForm):
    class Meta:
        model = Cars
        fields = "__all__"
