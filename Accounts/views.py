# accounts/views.py

import django.core
import django.core.exceptions
import django.db
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from Accounts.models import RegisteredUsers
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from django.urls import reverse
import django
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .token import account_activation_token, token_generator
from django.core.mail import EmailMessage
from django.conf import settings


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == '' or password == '':
            messages.error(request, "Please Fill Up all the Fields..!!!! ", extra_tags='danger')
            return redirect('login')
        
        # Authenticate the user
        try:
            check_user_active = RegisteredUsers.objects.filter(username=username)
            user = RegisteredUsers.objects.get(username=username)
                
            if check_user_active.exists():
                user = RegisteredUsers.objects.get(username=username)
                if user.is_active == True:
                    user = authenticate(request, username=username, password=password)
                    if user is not None:
                        login(request, user)
                        messages.success(request, "Logged in Successfully ", extra_tags=f"Welcome {request.user.first_name} {request.user.last_name}")
                        return redirect('student_corner')
                    else:
                        messages.error(request, "Invalid Username or Password. Try Again..!!!!!", extra_tags='danger')
                elif user.is_active == False:
                    current_site = get_current_site(request)
                    mail_subject = 'Activate your account on JavaGurukul'
                    message = render_to_string('accounts/activate_email.html', {
                        'user': user,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': account_activation_token.make_token(user),
                    })
                    email = EmailMessage(
                        mail_subject,   
                        message,        # HTML Content
                        to=[user.email]   # Recipient
                    )
                    email.content_subtype = "html"  # Set the content type to HTML
                    email.send()

                    messages.error(request, "Your Account is not active. Please Check Your mail to activate")
                    redirect('login')
                else:
                    messages.error(request, "Something Went Wrong...")
                    redirect('login')
            else:
                messages.error(request, "Account Does not Exists....!!")
                redirect('login')

        except django.core.exceptions.ObjectDoesNotExist:
            messages.error(request, 'Username Does not exists....!')
            redirect('login')
            

    return render(request, "accounts/login.html", {})


def Register(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname') 
        username = request.POST.get('username') 
        email = request.POST.get('email') 
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')

        if not all([firstname, lastname, username, email, password, cpassword]):
            messages.error(request, "Please fill in all the fields.", extra_tags='danger')
            return redirect('register')

        if password != cpassword:
            messages.error(request, "Passwords don't match.")
            return redirect('register')

        try:
            user = RegisteredUsers.objects.create_user(username=username, email=email, password=password)
            user.first_name = firstname
            user.last_name = lastname
            user.is_active = False  
            # user.save()

            current_site = get_current_site(request)
            mail_subject = 'Activate your account on JavaGurukul'
            message = render_to_string('accounts/activate_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            email = EmailMessage(
                mail_subject,   
                message,        # HTML Content
                to=[email]   # Recipient
            )
            email.content_subtype = "html"  # Set the content type to HTML
            email.send()

            user.save()
            messages.success(request, "An Confirmation Link is Sent on your mail....")
            return redirect('login') 

        except django.db.utils.IntegrityError:
            messages.error(request, 'User already exists. with this username or email....!!')
            return redirect('register')

        except Exception as e:
            messages.error(request, str(e))
            return redirect('register')

    return render(request, 'accounts/register.html')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = RegisteredUsers.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, RegisteredUsers.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.is_staff  = False
        user.is_superuser = False
        user.save()
        login(request, user)
        return HttpResponse('<h1 style="color:#309255">Thank you for your email confirmation. Now you can login your account.</h1>')
    else:
        return HttpResponse('Activation link is invalid!')
    

def UserLogout(request):
    logout(request)
    return redirect(reverse('login'))




from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User
from django.shortcuts import HttpResponse
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode
from .models import RegisteredUsers


def passwordReset(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email  = request.POST.get('email')
        if not  email:
            messages.error(request, "Please fill in all the fields.")
            print('Error')
            return redirect('password_reset')
        
        try:
            if RegisteredUsers.objects.filter(email = email).exists:
                user = RegisteredUsers.objects.get(email = email)
                print(user.email)
                
                current_site = get_current_site(request)
                mail_subject = 'Activate your account on JavaGurukul'
                message = render_to_string('accounts/reset_password_template.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': token_generator.make_token(user),
                })
                domain= current_site.domain,
                uid= urlsafe_base64_encode(force_bytes(user.pk)),
                token= token_generator.make_token(user),
                
                print(f'http://{domain[0]}/accounts/password-reset-token/{uid[0]}/{token[0]}')
                email = EmailMessage(
                    mail_subject,   
                    message,        # HTML Content
                    to=[email]   # Recipient
                )
                email.content_subtype = "html"  # Set the content type to HTML
                email.send()
                
            else:
                print("User Does Not Exists...")
                
        except Exception as e:
            print(e)
        
    return render(request, 'registration/password_reset_form.html')

def confirmToken(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = RegisteredUsers.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, RegisteredUsers.DoesNotExist):
        user = None
    if user is not None and token_generator.check_token(user, token):
        reset_password_token = {
            'user' : user,
            'uid' : uid,
            'token' : token,
            
            
        }
        return HttpResponse(f"{reset_password_token['user']}")
        
        
    else:
        return HttpResponse("Token is Invalid...........")

