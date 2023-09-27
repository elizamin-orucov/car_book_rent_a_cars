from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib import messages
from .forms import (
    LoginForm, RegisterForm, ActivateForm, CustomPasswordChangeForm,
    ResetPasswordForm, ResetPasswordCompleteForm, ProfileEditForm
)
from django.contrib.auth.decorators import login_required
from .decorators import not_authorized_user
from django.contrib.auth import update_session_auth_hash
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse_lazy
from Cars.models import CarsOrder


User = get_user_model()


@not_authorized_user
def login_view(request):
    next = request.GET.get("next", None)
    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request.POST or None)

        if form.is_valid():

            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(email=email, password=password)
            login(request, user)
            if next:
                return redirect(next)
            return redirect('/')

    context = {
        "form": form
    }
    return render(request, "users/login.html", context)


def logout_view(request):
    logout(request)
    return redirect('/')


def register_view(request):
    form = RegisterForm()

    if request.method == "POST":
        form = RegisterForm(request.POST or None)

        if form.is_valid():
            user = form.save()

            return redirect("users:activate", slug=user.slug)

    context = {
        "form": form
    }
    return render(request, "users/register.html", context)


def account_activate_view(request, slug):
    user = get_object_or_404(User, slug=slug)
    form = ActivateForm()
    message2 = ""

    if request.method == "POST":
        form = ActivateForm(request.POST or None)

        if form.is_valid():
            if form.cleaned_data.get("activation_code") == user.activation_code:
                form.save(commit=False)
                # login(request, user)
                user.is_active = True
                user.activation_code = None
                user.save()
                return redirect('users:login')

            else:
                messages.error(request, "Aktivasiya kodunu düzgün qeyd edin.")



    context = {
        "form": form
    }
    return render(request, "users/activate.html", context)

@login_required(login_url='/user/login/')
def password_change_view(request):
    form = CustomPasswordChangeForm(user=request.user)

    if request.method == "POST":
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/')

    context = {
        "form": form
    }
    return render(request, "users/password_change.html", context)


def reset_password_view(request):
    form = ResetPasswordForm()

    if request.method == "POST":
        form = ResetPasswordForm(request.POST or None)

        if form.is_valid():
            email = form.cleaned_data.get("email")
            user = User.objects.get(email=email)

            link = request.build_absolute_uri(reverse_lazy("users:reset-complete", kwargs={"slug": user.slug}))
            message = f"Please click the link below \n{link}"


            # send mail
            send_mail(
                'Reset password',  # subject
                message,  # message
                settings.EMAIL_HOST_USER,  # from email
                [email],  # to mail list
                fail_silently=False,
            )

            return redirect("/user/login/")

    context = {
        "form": form
    }
    return render(request, "users/reset.html", context)


def reset_password_complete_view(request, slug):
    user = get_object_or_404(User, slug=slug)
    form = ResetPasswordCompleteForm(instance=user)

    if request.method == "POST":

        form = ResetPasswordCompleteForm(instance=user, data=request.POST)

        if form.is_valid():
            form.save()
            return redirect("/user/login/")

    context = {
        "form": form
    }
    return render(request, 'users/reset_complete.html', context)


@login_required(login_url="users:login")
def profile_view(request):
    cars = CarsOrder.objects.filter(email=request.user.email)
    form = ProfileEditForm(instance=request.user)

    # car_wait = CarsOrder.objects.filter(email=request.user.email, status="Gözləmədə")
    # if request.method == "POST":
    #     form = ProfileEditForm(instance=request.user, data=request.POST, files=request.FILES)
    #     form.save()

    context = {"cars":cars, "form":form}
    return render(request,"users/profile.html", context)