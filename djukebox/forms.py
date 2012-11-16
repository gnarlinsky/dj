from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm 
from djukebox.models import Owner

class RegistrationForm(ModelForm):
    """ Django creates a form out of the fields in the passed-in ModelForm """
    username    = forms.CharField(label = (u'User Name') )
    email       = forms.EmailField(label = (u'Email Address') ) #Django will automatically validate
    password    = forms.CharField(label = (u'Password'), \
                    widget = forms.PasswordInput(render_value=False) )
                    # render_value=False: password won't be visible
                    # as it's entered
    password1   = forms.CharField(label = (u'Verify Password'), \
                    widget=forms.PasswordInput(render_value=False) )
                    # enter password twice

    class Meta:
        model = Owner # takes a model, makes form out of the fields
        exclude = ('user',) # exclude the user field
        #  ???????????????????????????????????  NOT SURE WHAT EXCLUDING FROM WHERE... 'user' is a field in the Owner model... but...what? so
        #   look here:
        #   https://www.google.com/url?url=https://docs.djangoproject.com/en/dev/topics/forms/modelforms/%23using-a-subset-of-fields-on-the-form&rct=j&q=django+forms.py+exclude+fields&usg=AFQjCNH9QIxVxQ11h8Izyb73K8_X6xha6Q&sa=X&ei=PYWlUIKKHcjgyQHlw4DACg&ved=0CDQQygQwAA

class LoginForm(forms.Form):
    username    = forms.CharField(label=(u'User Name'))
    password    = forms.CharField(label=(u'Password'), \
                    widget=forms.PasswordInput(render_value=False))
        
    """
    def clean_username(self):
        #Clean different members of the field, so if call form.is_valid, will see 
        #    if created a clean method for members of the form (username is Python object 
        #    at this point -- clean() has already cleaned the data once

        username = self.cleaned_data['username']

        try:
            # get user object that already has the user name that's been submitted through the form.....  
            #   I THINK  ?????????????????
            User.objects.get(username=username) 

        except User.DoesNotExist:
            # so, saying it's OK, just go ahead and use the user name you have....  
            #   Wait, WHAT????????????????????????
            return username 

        raise forms.ValidationError('That username is already taken. Please select another.') 

    ############# ????????????????????????????????
    #           So why isn't this called ....  clean_password(self), following the above?????  
    #           Look up what a general clean() should do............
    def clean(self):
        if self.cleaned_data['password'] != self.cleaned_data['password1']:
            raise forms.ValidationError('The passwords did not match. Please try again.')
"""

