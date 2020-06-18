from django import forms

class CreateArticle(forms.Form):
    PUBLISH = "publish"
    DRAFT = "draft"
    CHOICES = [("publish", PUBLISH), ("draft", DRAFT)]
    Title = forms.CharField(label='Title', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Title'}))
    Body = forms.CharField(label='Body', max_length=1000, widget=forms.TextInput(attrs={'placeholder': 'Body'}))
    Status = forms.ChoiceField(widget= forms.RadioSelect(), choices = CHOICES)