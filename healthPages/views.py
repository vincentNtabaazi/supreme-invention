from django.shortcuts import redirect, render
from . models import Appointment
from datetime import datetime
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
  return render(request, 'index.html')

def about_us(request):
  return render(request, 'about_us.html')

@login_required
def book_appointment(request):
  return render(request, 'book_appointment.html')

@login_required
def pending_appointment(request):
  appointmentList = []
  appointments = Appointment.objects.filter(user=request.user).order_by('id')
#   appointments = Appointment.objects.all()
  for appointment in appointments:
    appointmentList.append(appointment)
  context = {'appointments' : appointmentList}
  return render(request, 'pending_appointment.html', context)

@login_required
def save_appointment(request):
  if request.method =='POST':
    try:
      name = request.POST.get('name')
      mobileNo = request.POST.get('mobileNo')
      email = request.POST.get('email')
      user = request.user
      my_date_str = request.POST.get('app_date')
      app_date = datetime.strptime(my_date_str, "%m/%d/%Y").strftime("%Y-%m-%d")
      area = request.POST.get('area')
      district = request.POST.get('district')
      description = request.POST.get('description')
      ap=Appointment(fullname=name,mobileNo=mobileNo,email=email,user=user,appointmentDate=app_date,area=area,description=description,district=district)
      ap.save()
      return redirect('pending_appointment')
    except Exception as identifier:
      pass
  return render(request, 'book_appointment.html')

def RegistrationView(request):
    if request.method == "POST":
        context={
            'data':request.POST,
            'has_error':False,
        }
        email=request.POST.get('email')
        username=request.POST.get('username')
        full_name=request.POST.get('name')
        password=request.POST.get('password')
        password2=request.POST.get('password2')

        try:
            if len(password)<6:
                messages.add_message(request, messages.ERROR, 'Passwords should atleast be 6 characters long.')
                context['has_error']=True
        except Exception as identifier:
            pass

        if password != password2:
            messages.add_message(request, messages.ERROR, 'Passwords do not match.')
            context['has_error']=True

        try:
            if User.objects.get(email=email):
                messages.add_message(request, messages.ERROR, 'Email is taken.')
                context['has_error']=True
        except Exception as identifier:
            pass

        try:
            if User.objects.filter(username=username).first():
                messages.add_message(request, messages.ERROR, 'Username is taken.')
                context['has_error']=True
        except Exception as identifier:
            pass

        if context['has_error']:
            return render(request, 'register.html', context, status=400)
        
        user=User.objects.create_user(username=username, email=email)
        user.set_password(password)
        user.first_name=full_name
        user.last_name=full_name

        user.save()

        messages.add_message(request, messages.SUCCESS, 'Account is created successfully.')

        return redirect('login')
    return render(request, 'register.html')
    
def LoginView(request):
    if request.method == "POST":
        context={
            'data':request.POST,
            'has_error':False
        }
        username=request.POST.get('username')
        password=request.POST.get('password')
        
        
        try:
            user_details = User.objects.get(username=username)
            email = user_details.email
            user_email = User.objects.get(email=email)
            if not user_email.is_active:
                messages.add_message(request, messages.ERROR, 'Check your email to verify your account.')
        except Exception as identifier:
            pass

        if username=='':
            messages.add_message(request,messages.ERROR, 'Username is required.')
            context['has_error']=True

        if password=='':
            messages.add_message(request,messages.ERROR, 'Password is required.')
            context['has_error']=True

        user=authenticate(request, username=username, password=password)

        if not user and not context['has_error']:
            messages.add_message(request,messages.ERROR, 'Invalid login.')
            context['has_error']=True

        if context['has_error']:
            return render(request, 'login.html', status=401, context=context)
        
        login(request, user)
        return redirect('index')
    return render(request, 'login.html')
    
def LogoutView(request):
    if request.method == "GET":
        logout(request)
        messages.add_message(request,messages.SUCCESS, 'Logged out successfully.')
        return render(request, 'login.html')