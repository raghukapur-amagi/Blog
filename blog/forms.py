from django import forms

class CreateArticle(forms.Form):
    publish = "publish"
    draft = "draft"
    choices = [("publish", publish), ("draft", draft)]
    Title = forms.CharField(label='Title', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Title'}))
    Body = forms.CharField(label='Body', max_length=1000, widget=forms.TextInput(attrs={'placeholder': 'Body'}))
    Status = forms.ChoiceField(widget= forms.RadioSelect(), choices = choices)