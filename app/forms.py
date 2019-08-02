from django import forms
from django.contrib.auth.models import User
from .models import Profile, ContactMessage, phone_regex, Pledge

class ProfileForm(forms.ModelForm):

    momo_name = forms.CharField(
        max_length=20,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Momo name...'
            }
        )
    )

    date_of_birth = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'placeholder': 'Date of birth',
                'type':'date'
            }
        )
    )

    class Meta:
        model = Profile
        fields = (
            'momo_name',
            'date_of_birth',
            'picture',
        )

class ProfileEditForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'placeholder': 'Date of birth',
                'type':'date'
            }
        )
    )
    picture = forms.ImageField(
        label = "Profile Picture",
        required=False,
        widget=forms.FileInput()
     )

    class Meta:
        model = Profile
        fields = (
            'date_of_birth',
            'picture',
        )


class UserCreateForm(forms.ModelForm):
    username = forms.CharField(
        validators=[phone_regex,],
        label = 'Momo number',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'momo number...'
            }
        )
    )
    password = forms.CharField(
        max_length=20,
        widget=forms.PasswordInput(
            attrs={
                "placeholder":"Password...",
            }
        )
    )
    password2 = forms.CharField(
        max_length=20,
        widget=forms.PasswordInput(
            attrs={
                "placeholder":"Repeat password..."
            }
        )
    )
    class Meta:
        model = User
        fields = ('username','password',)

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password2'] != cd['password']:
            raise forms.ValidationError("The Passwords do not match")
        else:
            return cd['password2']

class LoginForm(forms.Form):
    username = forms.CharField(
        label = 'Momo name',
        validators=[phone_regex,],
        max_length=14,
        widget=forms.TextInput(
            attrs={
                'placeholder':'Momo number',
            }
        )
    )
    password = forms.CharField(
        max_length=20,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password',
            }
        )
    )


class ContactForm(forms.Form):
    phone_number = forms.CharField(

        validators=[phone_regex,],
        max_length=14,
        widget=forms.TextInput(
            attrs={
                'placeholder':'Phone number',
            }
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Email'
            }
        )
    )

    class Meta:
        fields = ('phone_number', 'email', 'message')


class PledgeForm(forms.ModelForm):
    amount = forms.IntegerField(
        widget = forms.NumberInput(
            attrs={
                'placeholder': 'Amount in Cedis'
            }
        )
    )
    class Meta:
        model = Pledge
        fields = ('amount',)

class MomoRefNumberForm(forms.ModelForm):
    reference_number = forms.CharField(
        max_length=20,
        widget = forms.TextInput(
            attrs={
                'placeholder': 'Enter Momo Payment Reference Number',
            }
        )
    )
    class Meta:
        model = Pledge
        fields = ('reference_number', )