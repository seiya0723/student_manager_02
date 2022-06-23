from django import forms
from .models import Building

class BuildingForm(forms.ModelForm):
    class Meta:
        model = Building
        fields = ["name", "description"] # descriptionはチェック不要と思うが一応