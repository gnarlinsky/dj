from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm # so can just pass a model and Django will create a form out of the fields in the model
from djukebox.models import Owner

class RegistrationForm(ModelForm):
    username    = forms.CharField(label=(u'User Name'))
    email       = forms.EmailField(label=(u'Email Address')) #Django will automatically validate
    password    = forms.CharField(label=(u'Password'), \
                    widget = forms.PasswordInput(render_value=False))
                    # render_value=False: password won't be visible
                    # as it's entered

    password1   = forms.CharField(label=(u'Verify Password'), \
                    widget=forms.PasswordInput(render_value=False))
                    # enter password twice

    class Meta:
        model = Owner # takes a model, makes form out of the fields
        # so this is why birthday, etc. not here, because it's
        # already in the model for Owner?  but ... aren't username
        # and email in there too?  answer: NOPE - just user,
        # birthday, and name are in there....  but....why aren't
        # username and email in there also? I don't understand why
        # those things don't get stored in Owner model as well?
        # What is the connection between Django's User model and my
        # Owner model? 
        
        exclude = ('user',) # exclude the user field
        #  arghhh  WHY!!!!!!
        
    """
    def clean_username(self):
    # Clean different members of the field, so if call form.is_valid, will see if created a clean method for members of the form (username is Python object at this point; clean() has already cleaned the data once
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username) # get user object that already has the user name that's been submitted through the form.....  I THINK  ?????????????????
        except User.DoesNotExist:
            return username # so, saying it's OK, just go ahead and use the user name you have....  Wait, WHAT????????????????????????
        raise forms.ValidationError('That username is already taken. Please select another.') 


    def clean(self):
        if self.cleaned_data['password'] != self.cleaned_data['password1']:
            raise forms.ValidationError('The passwords did not match. Please try again.')

"""


class LoginForm(forms.Form):
    username    = forms.CharField(label=(u'User Name'))
    password    = forms.CharField(label=(u'Password'), \
                    widget=forms.PasswordInput(render_value=False))


