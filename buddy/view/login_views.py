"""Module containing all view functions for login"""
import re
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpRequest
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password, ValidationError


def index(request):
    """ Returns the login and registration view """
    return render(request, 'account/login.html')

def login_view(request):
    """ Endpoint for login """
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('buddy:index'))
        else:
            return render(request, 'account/login.html', {
                'error_message': "Ugyldig brukernavn eller passord",
            })
    else:
        return render(request, 'account/login.html')


def register_view(request: HttpRequest):
    """ Endpoint for registering a user """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        is_professor = is_professor_set_in_post(request)

        error_messages = validate_registration_info(username, password, email, is_professor)

        if error_messages:
            return render(request, 'account/register.html', error_messages)

        user = User.objects.create_user(username=username, email=email, password=password)
        user.profile.is_professor = is_professor
        user.profile.save()

        login(request, user)
        return HttpResponseRedirect(reverse('buddy:index'))
    else:
        return render(request, 'account/register.html')

def is_valid_username(username: str):
    if User.objects.filter(username=username):
        # Username is already in use
        return False
    else:
        return True

def is_valid_password(password: str):
    try:
        validate_password(password)
        return True
    except ValidationError:
        return False

def is_valid_email(email_adress: str):
    """
    Validates an e-mail address

    Vaidates an e-mail by matching it against a regex expression that catches almost
    all possible valid e-mails. Raises a ValueError if the e-mail is invalid, otherwise
    it returns void.
    """
    pattern = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
    if pattern.match(email_adress) is None:
        return False
    else:
        return True

def is_professor_set_in_post(request: HttpRequest):
    try:
        request.POST['professor']
        return True
    except Exception:
        return False

def is_valid_professor_registration(email: str, is_professor: bool):
    # TODO: Should perform some form of auth
    return True

def validate_registration_info(username: str, password: str, email: str, is_professor: bool):
    error_messages = {}
    if not is_valid_username(username):
        error_messages["username"] = "Invalid username"
    if not is_valid_password(password):
        error_messages["password"] = "Invalid password. You need to have both upper and lower case letters"
    if not is_valid_email(email):
        error_messages["email"] = "Invalid email. Make sure yuo included the full e-mail"
    if not is_valid_professor_registration(email, is_professor):
        error_messages["professor"] = "Invalid professor email, are you sure you are a professor?"
    return error_messages
