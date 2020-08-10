from django import forms
from .models import Item

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = '__all__'
    def clean_user(self):
        if not self.cleaned_data['user']:
            return User()
        return self.cleaned_data['user']
