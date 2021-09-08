from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserChangeForm
from account.models import Address
from account.models.custom_user import CustomUser
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm


class HiddenRedirectForm(forms.Form):
    redirect_after_delete_item = forms.CharField(required=False,
                                                 widget=forms.HiddenInput(
                                                     attrs={
                                                         'id': 'redirect_after_delete_item'
                                                     })
                                                 )


class CustomAuthenticationForm(AuthenticationForm):
    """
    Login
    """

    def __init__(self, *args, **kwargs):
        super(CustomAuthenticationForm, self).__init__(*args, **kwargs)

    email = forms.EmailField(max_length=50, label='Email', help_text='', widget=forms.EmailInput(
        attrs={'class': 'input-custom shadow appearance-none border rounded w-full py-2 px-3 text-grey-darker'}))
    password = forms.CharField(max_length=50, label='Mot de passe', widget=forms.PasswordInput(
        attrs={'class': 'input-custom shadow appearance-none border rounded w-full py-2 px-3 text-grey-darker',
               }
    ))

    class Meta:
        model = CustomUser
        fields = ['email', 'password', ]


class AddressCreationForm(forms.ModelForm):
    street = forms.CharField(max_length=50, label="Rue ...", widget=forms.TextInput(
        attrs={'class': 'input-custom w-full'}))
    apartment = forms.CharField(max_length=50, label="Suite adresse", required=False, widget=forms.TextInput(
        attrs={'class': 'input-custom w-full'}))
    zip = forms.CharField(max_length=50, label="Code Postal", widget=forms.TextInput(
        attrs={'class': 'input-custom w-full'}))
    city = forms.CharField(max_length=50, label="Ville", widget=forms.TextInput(
        attrs={'class': 'input-custom w-full'}))

    class Meta:
        model = Address
        fields = ['street', 'apartment', 'zip', 'city']


class CustomUserCreationForm(UserCreationForm):
    """
    Part
    """
    email = forms.EmailField(max_length=50, label='Email', help_text='', widget=forms.EmailInput(
        attrs={'class': 'input-custom w-full'}))
    phone = forms.CharField(label='Telephone', widget=forms.TextInput(
        attrs={'class': 'input-custom w-full'}))
    last_name = forms.CharField(max_length=50, label="Nom de famille", widget=forms.TextInput(
        attrs={'class': 'input-custom w-full'}))
    first_name = forms.CharField(max_length=50, label="Prénom", widget=forms.TextInput(
        attrs={'class': 'input-custom w-full'}))
    password1 = forms.CharField(max_length=50, label='Mot de passe', widget=forms.PasswordInput(
        attrs={'class': 'input-custom w-full'}))
    password2 = forms.CharField(max_length=50, label='Confirmation mot de passe', widget=forms.PasswordInput(
        attrs={'class': 'input-custom w-full'}))

    class Meta:
        model = CustomUser
        fields = ['email', 'phone', 'last_name', 'first_name', 'password1',
                  'password2']


class CustomUserChangeForm(UserChangeForm):
    """
    ADMIN Site
    """

    class Meta:
        model = CustomUser
        fields = ('email',)


class CustomUserUpdateForm(forms.ModelForm):
    """
    Update user
    """

    email = forms.EmailField(max_length=50, label='Email', help_text='', widget=forms.EmailInput(
        attrs={'class': 'input-custom w-full'}))

    phone = forms.CharField(label='Telephone', widget=forms.TextInput(
        attrs={'class': 'input-custom w-full'}))
    last_name = forms.CharField(label='Nom', widget=forms.TextInput(
        attrs={'class': 'input-custom w-full'}))
    first_name = forms.CharField(label='Prénom', widget=forms.TextInput(
        attrs={'class': 'input-custom w-full'}))

    class Meta:
        model = CustomUser
        fields = ['email', 'phone', 'last_name', 'first_name']


class UserPasswordResetForm(SetPasswordForm):
    """Change password form."""
    new_password1 = forms.CharField(label='Mot de passe',
                                    help_text="",
                                    max_length=100,
                                    required=True,
                                    widget=forms.PasswordInput(
                                        attrs={
                                            'class': 'input-custom w-full',
                                            'type': 'password',
                                            'id': 'user_password',
                                        }))

    new_password2 = forms.CharField(label='Confirmation',
                                    help_text=False,
                                    max_length=100,
                                    required=True,
                                    widget=forms.PasswordInput(
                                        attrs={
                                            'class': 'input-custom w-full',
                                            'type': 'password',
                                            'id': 'user_password',
                                        }))
