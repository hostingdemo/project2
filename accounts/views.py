import datetime
from django.core.mail import EmailMessage
from django.contrib.auth.mixins import PermissionRequiredMixin

from django.http.response import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.db.models.query_utils import Q

from schools.models import *
from django.views import View
from django.contrib.sites.models import Site

from django.views.generic import ListView
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages #import messages
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import Permission
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.template.loader import render_to_string
from .utils import account_activation_token
from django.urls import reverse
from django.contrib import auth
from .models import *
User = get_user_model()

from django.http import JsonResponse
from django.middleware.csrf import rotate_token

def login_view(request):
    if request.is_ajax and request.method == "POST":
        print('i am here')
        username = request.POST.get('email')
        password = request.POST.get('password')
        remember_me = request.POST.get('rememberme')

        if not remember_me:
            request.session.set_expiry(0)

        if username == '' or password == '':
            return JsonResponse({'message': 'Please  provide email and password'}, status=400)
        
        user=authenticate(request, username=username, password=password)

        if user is not None:
            print('here2')

            if user.is_staff:
                login(request, user)
                return HttpResponseRedirect(reverse('employee_dashboard'))

            elif user.is_school:
                print('here3')
                login(request, user)
                rotate_token(request)
                return redirect('school_dashboard')


            else:
                print('here4')

                login(request, user)
                rotate_token(request)

                return HttpResponseRedirect(reverse('my_account'))

        else:
            return JsonResponse({
                    "message": "Please enter a correct email and password. Note that both fields may be case-sensitive"
                }, status=400)
    return JsonResponse({'message': 'Method not allowed'}, status=400)

def logout_view(request):
    logout(request)
    return redirect('home')


def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "main/password/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain': send_school_activation_mail,
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
                    'site' : get_current_site(request).domain,
					}



					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'admin@JDMR_ischool.com' , [user.email], fail_silently=False)
					except BadHeaderError:

						return HttpResponse('Invalid header found.')
						
					messages.success(request, 'A message with reset password instructions has been sent to your inbox.')
					return redirect ("done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="main/password/password_reset.html", context={"password_reset_form":password_reset_form})

# code for sending reset passord link for school after activating their account
def password_reset_school(request, email):

    print('hey i am here')
	
    data = email
    associated_users = User.objects.filter(Q(email=data))
    if associated_users.exists():
        for user in associated_users:
           

            link = 'http://127.0.0.1:8000/accounts/reset/' + urlsafe_base64_encode(force_bytes(user.pk)) + '/' + default_token_generator.make_token(user) + '/'

            print('here to')
            print(link)
            return link

    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="main/password/password_reset.html", context={"password_reset_form":password_reset_form})



def signup_student(request):

    if request.user.is_authenticated:
        return redirect('home')
        
    if request.is_ajax and request.method == "POST":
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        remember_me = request.POST.get('rememberme')

        if not remember_me:
            request.session.set_expiry(0)

        if email == '' or password1 == '' or password2 == '':
                return JsonResponse({'message': 'Please provide valid inputs'}, status=400)
                
        if len(password1) < 6:
            return JsonResponse({"message": "Password is to short"}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({"message": "User already exists"}, status=400)
        else:
            if password1 == password2:
                # data = {'email':email, 'password2':password2, 'password1':password1}
                account = User.objects.create_user(email=email, password=password1)
                account.save()
                login(request, account)
                rotate_token(request)
                return JsonResponse({"message": "Success"}, status=200)
            else:
                return JsonResponse({"message": "password didn't matched"}, status=400)
    
    return JsonResponse({"message": "Denied"})
    


class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            print('1')
            id = force_text(urlsafe_base64_decode(uidb64))
            print('2')

            user = User.objects.get(pk=id)
            print('3')


            if not account_activation_token.check_token(user, token):
                return redirect('login'+'?message='+'User already activated')
            print('4')

            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.is_school = True
            user.save()

            print('5')

           

            data = SchoolRegistration.objects.get(user = user)
            instance = School.objects.get(id = data.school.id)
            instance.owner = user
            instance.save()

            messages.success(request, 'Account activated successfully')

            a = password_reset_school(request, user.email)

            print('6')
            
            return HttpResponseRedirect(a)

        except Exception as ex:
           
        
            print('-------------------2--------------')

            return redirect('login')


def school_registration(request):

    if request.method == "POST":

        email = request.POST.get('school-email')
        
        print(email)
        name = request.POST.get('name')
        print(name)
        contact_number = request.POST.get('contact_number')
        print(contact_number)
        password = "ohsifhdhfhiAisHHDi@12"
        test1 = User.objects.create_user(email=email, password=password)
        
        test1.is_active = False # bro yaha par vailadtors laga de n password is short wagre wagre
                         

        if test1:
            print('---------------------------------------------------')
            print(request.user)
            
            school_id = request.POST.get('school')
            print('--------------------------')
            print(school_id)
            school_data = School.objects.get(id = school_id)
            SchoolRegistration.objects.create(user=test1, email=email, name=name, contact_number=contact_number, school = school_data)
            test1.save()   #saving user only if school data table make changes
            # send msg with it you will shortly recieve a call from our assocaiate
            return HttpResponseRedirect(reverse('home'))

        else:
            return HttpResponseRedirect(reverse('home'))
    else:
        dropdown_data = School.objects.all().order_by('school_name')
        return render(request, 'accounts/school_registration.html', {'dropdown_data' : dropdown_data})

class SchoolRequests(PermissionRequiredMixin, ListView):
    permission_required = 'accounts'
    model = SchoolRegistration
    template_name = 'schools/school_requests.html'
    paginate_by = 20 # if pagination is desired
    permission_required = 'accounts'
    login_url = 'home'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def send_school_activation_mail(request, uid):

    user = User.objects.get(id = uid)
    email = user.email

    current_site ='127.0.0.1:8000/'
    email_body = {
        'user': user,
        'domain':'127.0.0.1:8000',
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    }

    link = reverse('activate', kwargs={
                'uidb64': email_body['uid'], 'token': email_body['token']})

    email_subject = 'Activate your account'

    activate_url = current_site+link

    email = EmailMessage(
        email_subject,
        'Hi '+user.email + ', Please the link below to activate your account \n'+activate_url,
        'noreply@jdmr.com',
        [email],
    )

    if email:
        emails_record.objects.create(to = user.email, link = activate_url)
    print('---------------------------------------')
    print(email)
    email.send(fail_silently=False)

    return HttpResponseRedirect(reverse('school_requests'))


def create_employee(request):

    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == "POST":
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
     

        if email == '' or password1 == '' or password2 == '':
            print('Please provide valid inputs')
            return HttpResponseRedirect(reverse('create_employee'))

                
        if len(password1) < 6:
            print("Password is to short")
            return HttpResponseRedirect(reverse('create_employee'))


        if User.objects.filter(email=email).exists():
            print("User already exists")
            return HttpResponseRedirect(reverse('create_employee'))

        else:
            if password1 == password2:
                # data = {'email':email, 'password2':password2, 'password1':password1}
                account = User.objects.create_user(email=email, password=password1, is_staff = True)
                account.save()

                permission1 = Permission.objects.get(name='Can view school')
                permission2 = Permission.objects.get(name='Can delete school')
                permission3 = Permission.objects.get(name='Can change school')
                permission4 = Permission.objects.get(name='Can add school')
                permission5 = Permission.objects.get(name='Can add school detail')
                permission6 = Permission.objects.get(name='Can change school detail')
                permission7 = Permission.objects.get(name='Can delete school detail')
                permission8 = Permission.objects.get(name='Can view school detail')
                permission9 = Permission.objects.get(name='Can change school facilities')
                permission10 = Permission.objects.get(name='Can add school facilities')
                permission11 = Permission.objects.get(name='Can view school facilities')
                permission12 = Permission.objects.get(name='Can delete school facilities')
                permission13 = Permission.objects.get(name='Can change school fee')
                permission14 = Permission.objects.get(name='Can add school fee')
                permission15 = Permission.objects.get(name='Can view school fee')
                permission16 = Permission.objects.get(name='Can delete school fee')
                permission17 = Permission.objects.get(name='Can change school gallery')
                permission18 = Permission.objects.get(name='Can add school gallery')
                permission19 = Permission.objects.get(name='Can delete school gallery')
                permission20 = Permission.objects.get(name='Can view school gallery')

                user = User.objects.get(email=email)
                print(user)
            
                user.user_permissions.add(permission1)
                user.user_permissions.add(permission2)
                user.user_permissions.add(permission3)
                user.user_permissions.add(permission4)
                user.user_permissions.add(permission5)
                user.user_permissions.add(permission6)
                user.user_permissions.add(permission7)
                user.user_permissions.add(permission8)
                user.user_permissions.add(permission9)
                user.user_permissions.add(permission10)
                user.user_permissions.add(permission11)
                user.user_permissions.add(permission12)
                user.user_permissions.add(permission13)
                user.user_permissions.add(permission14)
                user.user_permissions.add(permission15)
                user.user_permissions.add(permission16)
                user.user_permissions.add(permission17)
                user.user_permissions.add(permission18)
                user.user_permissions.add(permission19)
                user.user_permissions.add(permission20)
            
                print("done")
                return HttpResponseRedirect(reverse('create_employee'))
               
            else:
                print("password didn't matched")
                return HttpResponseRedirect(reverse('create_employee'))

      

    else:
        return render(request, 'accounts/add_employee.html')







