from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from users.models import User
from django.contrib.auth.forms import PasswordChangeForm
from users.forms import LoginForm, SignUpForm, UpdateForm


@api_view()
@permission_classes([permissions.IsAuthenticated])
def get_user(request):
    return Response(request.user.to_json())


def delete_user(request):
    if request.user.is_authenticated:
        user = request.user
        User.objects.filter(id=user.id).delete()
        return redirect('/logout/')
    else:
        return redirect('/home/')


@login_required
def show_user(request):
    return render(request, 'user/user.html', {'isSocial': request.user.isSocial()})


@login_required
def update_user(request):
    if request.user.isSocial():
        return redirect('/user')
    if request.method == 'POST':
        form = UpdateForm(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/user')
    else:
        form = UpdateForm(initial={field: getattr(request.user, field) for field in UpdateForm.Meta.fields})
    return render(request, 'user/update.html', {'form': form})


@login_required
def change_password(request):
    if request.user.isSocial():
        return redirect('/user')
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/user')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'user/change_password.html', {'form': form})


def user_signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/home')
    else:
        form = SignUpForm()
    return render(request, 'user/signup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                return redirect('/home/')
            else:
                return redirect('/user/login/?fail')
    else:
        form = LoginForm()
    return render(request, 'user/login.html', {'form': form})