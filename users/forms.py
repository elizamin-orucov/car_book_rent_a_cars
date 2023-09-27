from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.forms import UserCreationForm as BaseCreationForm
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings
from services.generator import CodeGenerator
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.hashers import check_password

User = get_user_model()

# -----------------------   Admin Forms  ---------------------------------------------------


class UserAdminCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = [
            "email",
            "full_name",
            "password1",
            "password2",
        ]

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            self.add_error("password1","Şifrələr arasında ziddiyyət var.")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = [
            "email",
            "full_name",
            "is_active",
            "is_superuser",
            "password",
        ]

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]




# Login Form

class LoginForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("email", "password")

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if User.objects.filter(email=email):
            user = User.objects.get(email=email)
            userpass = check_password(password,user.password)
            if password==None:
                self.add_error("password","Şifrəni qeyd edin.")
            elif userpass:
                if not user.is_active:
                    self.add_error("email","User aktiv deil.")
            else:
                self.add_error("email","Email və ya şifrə yanlışdır.")
        elif email==None:
            self.add_error("email","Email qeyd edin.")

        else:
            self.add_error('email', "Email və ya şifrə yanlişdır.")

        return self.cleaned_data



    def __init__(self, *args, **kwargs):
        palceholders={"email":"Mail ünvanı","password":"Şifrə"}
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                "class": "form-control","placeholder":f"{palceholders[field]}"
            })


class RegisterForm(UserAdminCreationForm):

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(RegisterForm, self).save()
        user.set_password(self.cleaned_data.get("password1"))
        user.is_active = False
        user.activation_code = CodeGenerator.create_activation_link_code(
            size=4, model_=User
        )
        if commit:
            user.save()

        message = f"Aktivasiya kodunuz: \nKod: - {user.activation_code}"
        # send mail
        send_mail(
            'CarBook Activate email', # subject
            message, # message
            settings.EMAIL_HOST_USER, # from email
            [user.email], # to mail list
            fail_silently=False,
        )
        return user

    def __init__(self, *args, **kwargs):
        palceholders = {"email": "Mail daxil edin", "password1": "Şifrə","password2": "Şifrə təkrarı","full_name":"Ad daxil edin"}
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                "class": "form-control", "placeholder": f"{palceholders[field]}","required":True
            })


class ActivateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ("activation_code", )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["activation_code"].widget.attrs.update({
            "class": "form-control", "placeholder": "Aktivasiya kodunu daxil edin"
        })


class CustomPasswordChangeForm(PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        placeholders={"old_password":"Köhnə şifrə","new_password1":"Yeni şifrə","new_password2":"Yeni şifrə təkrarı"}
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control","placeholder":f"{placeholders[field]}"})


class ResetPasswordForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email", )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control","placeholder":"Mailinizi daxil edin."})

    def clean(self):
        email = self.cleaned_data.get("email")
        if not User.objects.filter(email=email).exists():
            self.add_error("email","Mail ünvanı yanlışdır. İstifadəçi tapılmadı.")
        return self.cleaned_data


class ResetPasswordCompleteForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ("password1", "password2")

    def __init__(self, *args, **kwargs):
        placeholders={"password1":"Yeni şifrə","password2":"Yeni şifrə təkrarı"}
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control","placeholder":f"{placeholders[field]}"})

    def clean(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if len(password1.strip()) < 8:
            self.add_error("password1","Şifrənin uzunluğu 7-dən böyük olmalıdır")

        if password1 != password2:
            self.add_error("password1","Şifrələr arasında ziddiyət var.")

        return self.cleaned_data

    def save(self):
        password1 = self.cleaned_data.get("password1")
        self.instance.set_password(password1)
        self.instance.save()
        return self.instance


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("logo", )