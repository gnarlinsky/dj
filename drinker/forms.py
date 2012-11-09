from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm  # so can just pass a model and Django will create a form out of the fields in the model
from drinker.models import Drinker

class RegistrationForm(ModelForm):
    username        = forms.CharField(  label=(u'User Name'))
    email           = forms.EmailField( label=(u'Email Address'))   # Django will automatically validate
    password        = forms.CharField(  label=(u'Password'), \
                                widget=forms.PasswordInput(render_value=False))  
                                        # render_value=False: password won't be visible as entered
    password1       = forms.CharField(  label = (u'Verify Password'), \
                                widget=forms.PasswordInput(render_value=False))


######################  nk question ?????????? ##############
# why isn't 'birthday', etc., in here?????

    class Meta:
        model = Drinker  # takes a model, makes form out of the fields
        exclude = ('user',)  # but...  exclude the user field... 
        # WAIT SHOULDN'T THAT BE username ???????????  Or is that Django's that's called 'user'???
        
    def clean_username(self):
        """ Clean different members of the field. so if call form.is_valid, will see if created a 
        clean method for members of the form """
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)  # get user object that already has the user name that's been submitted through the form.... I think........
        except User.DoesNotExist:
            return username   # so saying it's okay, just go ahead and use the username you have
        raise forms.ValidationError('That user name is already taken. Please select another.')  # otherwise, 
   

   # what uses clean!!!!!! where?????????????
    def clean(self):
        if self.cleaned_data['password'] != self.cleaned_data['password1']:
            raise forms.ValidationError('The passwords did not match. Please try again.')
        return self.cleaned_data


class LoginForm(forms.Form):
    username        = forms.CharField(label=(u'User Name'))
    password        = forms.CharField(label = (u'Password'), widget=forms.PasswordInput(render_value=False))
