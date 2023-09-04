import six
import jwt
import datetime
from .forms import *
from .models import *
from django.views import View
from django.conf import settings 
from datetime import date,timezone
from django.contrib import messages
from django.http import HttpResponse
from django.core.mail import send_mail
from .decorators import validate_jwt_token
from django.shortcuts import render , redirect
from django.core.exceptions import ValidationError 
from django.template.loader import render_to_string 
from django.utils.encoding import force_str , force_bytes 
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.password_validation import validate_password
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.contrib.auth import get_user_model ,authenticate ,login ,logout

# Create your views here.

class TokenGenerate(PasswordResetTokenGenerator):
    
    # Make hash Values using AbstractBaseUser Current TimeStamp And user Is active 
    def _make_hash_value(self, user: AbstractBaseUser ,timestamp: int) -> str:
        return ( six.text_type(user) + six.text_type(timestamp) + six.text_type(user.is_active) )
    
# object  TokenGenerate
account_activate_token = TokenGenerate()


# creating jwt token 

def generate_jwt_token(user):
    print(user , "###################User")
    payload = {
        'email' : user.email ,
        'exp' : datetime.datetime.now() + datetime.timedelta(days=1)
    }
    token = jwt.encode(payload , 'secret' , algorithm='HS256')
    return token
    





#  User token send View
def UserAccountRegisterView(request):
    if request.user.is_authenticated:
        return redirect('Dashboard')
    else:
        if request.method == "POST":
            
            # get form with post request 
            form = CustomUserRegisterForm(request.POST)
            
            # check if form is valid or not 
            if form.is_valid():
                
                # save form with its instance 
                user = form.save(commit=False)
    
                # get form fields using cleaned data 
                Email = form.cleaned_data.get('email')
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                Confpassword = form.cleaned_data.get('confPassword')
                
                
                # check if password and confirm password are same 
                if password != Confpassword:
                    messages.warning(request , 'Password Not matching')
                    return render(request , 'UserRegister.html')
                
                try: 
                    # Validate the password against Django's password validation rules
                    validate_password(password , user=user )
    
                    # set user password in hash format using set_password function 
                    user.set_password(password)
                    user.is_active = False
                    user.save()
                    
                except ValidationError as errors:
                    for error in errors:
                        messages.warning(request , error)
                        return redirect('UserAccountRegisterView')
    
                # get current site domain 
                Current_site = get_current_site(request)
                
                # try to create hash token with user id 
                try:
                    subject = 'Account Activation Token link'
                    message = render_to_string('account_active_email.html', {  
                    'user': user,  
                    'domain': Current_site.domain,  
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)), 
                    'token':account_activate_token.make_token(user),  
                    'date': date.today()
                    })
                    from_email = settings.EMAIL_HOST_USER
                    recipient_list = [Email]
                    
                    # send mail using send_mail function django 
                    send_mail(subject , message , from_email , recipient_list)
                    
                    # return HttpResponse to user to check his gamil with validation link 
                    return HttpResponse('Please confirm your email address to complete the registration')
                
                except Exception as error:
                    # showing error to user 
                    messages.warning(request , error)
                    return render(request , 'UserRegister.html') 
            else:
                messages.warning(request , form.errors)
                return redirect('UserAccountRegisterView')
        else:
            # displaying form to user with get request 
            form = CustomUserRegisterForm()
            return render(request , 'UserRegister.html' , {'form':form})
        
        
    
    # User Token Check View 
def ActivateEmail(request , uidb64 , token):
    # get current user model 
    UserModel = get_user_model()
    
    try:
        # decode uidb64 to user id uid 
        uid = urlsafe_base64_decode(uidb64 + '==')
        uid = force_str(uid) 
        user = UserModel.objects.get(pk = uid)
    except (TypeError , ValueError , OverflowError , UserModel.DoesNotExist):
        user = None
        
        # check wheather the token or user is correct or not 
    if user is not None and account_activate_token.check_token(user , token):
        user.is_active = True
        user.save()
        messages.success(request, '✅ Email Verified')
        return redirect('UserAccountLoginView')
    else:
        # deleting the user instance from datatbse using delete method 
        user.delete()
        messages.warning(request, 'Invalid activation link.')
        return redirect('UserAccountRegisterView')
    

import random , math


    
    # User Login View 
def UserAccountLoginView(request):
    if request.user.is_authenticated:
        return redirect('Dashboard')
    else:
        if request.method == "POST":
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                
                
                # generate jwt token 
                jwt_token = generate_jwt_token(user)
                 
                # store jwt in sessions
                request.session['jwt_token'] = jwt_token
                
                # login user using django built in function
                login(request , user)
                
                messages.info(request, f'You are now logged in as {email}.')
                return redirect('Dashboard')
            else:
                messages.error(request, 'Invalid Crediential !')
                return render(request,'UserLogin.html')
        else:
            return render(request,'UserLogin.html')
        
    
@validate_jwt_token  
def Dashboard(request):
    return render(request , 'Dashboard.html')


def UserLogout(request):
    logout(request)
    # request.session['jwt_token_access'] = None
    return redirect('UserAccountLoginView')
 
    
        
        
            
        
    
        