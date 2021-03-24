from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
import bcrypt

def index(request):
    return render(request,'index.html')
def registration(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            if key == 'first_name' : 
                messages.error(request,value, extra_tags='first_name')
            if key == 'last_name' : 
                messages.error(request,value, extra_tags='last_name')
            if key == 'reg_email' : 
                messages.error(request,value, extra_tags='reg_email')
            if key == 'reg_password' : 
                messages.error(request,value, extra_tags='reg_password')
            if key == 'confirm_password' : 
                messages.error(request,value, extra_tags='confirm_password')
        return redirect('/')
    else:
        password = request.POST['reg_password']
        pw_hash = bcrypt.hashpw(request.POST['reg_password'].encode(), bcrypt.gensalt()).decode()
        user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['reg_email'],
            password = pw_hash
        )
        request.session['user_id'] = user.id 
        return redirect('/success')
def success(request):
    if 'user_id' not in request.session:
        return redirect("/")
    context = {
        'user' : User.objects.get(id=request.session['user_id'])
    }
    return render(request, "success.html", context)
def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            if key == 'log_email' : 
                messages.error(request,value, extra_tags='log_email')
            if key == 'log_password' : 
                messages.error(request,value, extra_tags='log_password')
        return redirect('/')
    else:
        user_list = User.objects.filter(email = request.POST['log_email'])
        if len(user_list) == 0:
            messages.error(request,"we could not find a  user with that email address", extra_tags='log_email')
        else:
            user = user_list[0]
            if bcrypt.checkpw(request.POST['log_password'].encode(), user.password.encode()):
                request.sesion['user_id'] = user_id
                return redirect('/success')
            else:
                messages.error(request, "your password was incorrect", extra_tags="log_password")
                return redirect('/')
                
    return redirect('/')
def logout(request):
    request.session.flush()
    return redirect('/')

