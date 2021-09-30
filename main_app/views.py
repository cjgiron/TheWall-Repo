from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Message, Comment
import bcrypt

def index(request):
    if "user_id" in request.session:
        return redirect('/dashboard')
    return render(request, "index.html")


def registration(request):
    errors = User.objects.registration_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')

    else: 
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        print(pw_hash)

        user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            birth_date = request.POST['birth_date'],
            password = pw_hash
        )
        
        request.session['user_id'] = user.id

        return redirect('/dashboard')


def login(request):
    errors = User.objects.login_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        
        return redirect('/')
    else:
        user = User.objects.get(email = request.POST['email'])
        request.session['user_id'] = user.id
        return redirect('/dashboard')


def dashboard(request):
    if "user_id" not in request.session:
        return redirect('/')

    context = {
        "user": User.objects.get(id = request.session['user_id']),
        "all_messages": Message.objects.all()
    }
    return render(request, "success.html", context)


def logout(request):
    request.session.flush()

    return redirect('/')



def process_message(request):
    print(request.POST)

    this_user = User.objects.get(id=request.POST['user_id'])

    Message.objects.create(
        message_text = request.POST['message'],
        user = this_user
    )

    return redirect('/dashboard')


def process_comment(request):
    print(request.POST)

    this_user = User.objects.get(id=request.POST['user_id'])
    this_message = Message.objects.get(id=request.POST['message_id'])

    Comment.objects.create(
        comment_text = request.POST['comment'],
        user = this_user,
        message = this_message
    )


    return redirect('/dashboard')
