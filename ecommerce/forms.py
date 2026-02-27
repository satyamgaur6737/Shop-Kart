from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,UsernameField,PasswordChangeForm,PasswordResetForm,SetPasswordForm
from django.contrib.auth.models import User
from ecommerce.models import Customer 
from django.contrib.auth import password_validation

class CustomerRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'class':'w-full px-4 py-2 mt-2 border rounded-md focus:outline-none focus:ring-1 focus:ring-blue-600 bg-gray-100'}))
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput(attrs={'class':'w-full px-4 py-2 mt-2 border rounded-md focus:outline-none focus:ring-1 focus:ring-blue-600 bg-gray-100'}))
    email =  forms.CharField(required=True,widget=forms.EmailInput(attrs={'class':'w-full px-4 py-2 mt-2 border rounded-md focus:outline-none focus:ring-1 focus:ring-blue-600 bg-gray-100'}))


    class Meta:
        model = User
        fields = ['username', 'email']
        labels ={'email':'Email'}
        widgets = {'username':forms.TextInput(attrs={'class':'w-full px-4 py-2 mt-2 border rounded-md focus:outline-none focus:ring-1 focus:ring-blue-600 bg-gray-100'})}


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus':True,
        'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
        'placeholder': 'Enter Username',
    }))
    
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete':'Current-password',
        'class': 'w-full px-4 py-2 border rounded-lg mt-4 focus:outline-none focus:ring-2 focus:ring-blue-500',
        'placeholder': 'Enter Password',
    }))        


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name','address','city','state','pincode']
        widgets = {
            'name': forms.TextInput(attrs={'class':'w-full border border-blue-500  rounded-lg px-3 py-2'}),
            'address': forms.TextInput(attrs={'class':'w-full border border-blue-500 rounded-lg px-3 py-2'}),
            'city': forms.TextInput(attrs={'class':'w-full border border-blue-500 rounded-lg px-3 py-2'}),
            'state': forms.Select(attrs={'class':'w-full border border-blue-500 rounded-lg px-3 py-2'}),
            'pincode': forms.TextInput(attrs={'class':'w-full border border-blue-500 rounded-lg px-3 py-2'}),
        }



class MyPasswordChangeForm(PasswordChangeForm):
    
    common_attrs = {
        'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
    }

    old_password = forms.CharField(
        label="Old Password",
        widget=forms.PasswordInput(attrs={**common_attrs, 'placeholder': 'Enter Old Password', 'autofocus': True})
    )
    
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={**common_attrs, 'placeholder': 'Enter New Password'})
    ,help_text=password_validation)
    
    new_password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(attrs={**common_attrs, 'placeholder': 'Confirm New Password'})
    )



class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=250,
        widget=forms.EmailInput(
            attrs={
                'class': 'w-full border border-gray-300 rounded-lg px-4 py-2 '
                         'focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Enter your email',
            }
        )
    )


class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label="New Password",widget=forms.PasswordInput( attrs={'class': 'w-full border border-gray-300 rounded-lg px-4 py-2 '
                         'focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500',
                'placeholder': 'Enter new password',
            }
        )
    )

    new_password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(
            attrs={
                'class': 'w-full border border-gray-300 rounded-lg px-4 py-2 '
                         'focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500',
                'placeholder': 'Confirm new password',
            }
        )
    )