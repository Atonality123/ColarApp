from django import forms

class MyForm(forms.Form):
    temperature = forms.CharField()
    pressure = forms.CharField()
    humidity = forms.CharField()	
    wind = forms.CharField()
    speed = forms.CharField()

class member(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
    submit_button = forms.CharField(widget=forms.HiddenInput(), initial='Submit', label="log in")