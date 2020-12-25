from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from users.models import User
from users.forms import LoginForm, SignUpForm

@api_view()
@permission_classes([permissions.IsAuthenticated])
def get_user(request):
    jsoned_user = {field.name: getattr(request.user, field.name) for field in User._meta.fields}
    jsoned_user.pop('password')
    return Response(jsoned_user)


def delete_user(request):
    if request.user.is_authenticated:
        user = request.user
        User.objects.filter(id=user.id).delete()
        return redirect('/logout/')
    else:
        return redirect('/home/')


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