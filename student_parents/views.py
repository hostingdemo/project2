from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponseRedirect
from django.http import JsonResponse
import json

from .forms import (
    StudentFrom,
    DocumentsFrom,
    AdditionalDetailsFrom,
    ParentDetailsFrom,
    ContactDetailsFrom
)

from .models import (
    Student,
    ContactDetails,
    AdditionalDetails,
    ParentDetails,
    Documents
)

from schools.models import School

User = get_user_model()


@login_required(login_url='login')
def student_list(request):

    student_list = Student.objects.filter(user = request.user)
    print(student_list)
    
    return render(request,  'student_parents/student_list.html', {'student_list' : student_list})



@login_required(login_url='login')
def profile(request):
    try:
        is_update_available = get_object_or_404(Student, user=request.user)
        if is_update_available:
            context = {
                'is_update_available':True,
                'is_student_detail_show':False
            }
    except:
        context = {
            'is_update_available':False,
            'is_student_detail_show':True
        }
    return render(request, 'student_parents/user_profile.html',context=context)

@login_required(login_url='login')
def profile_update(request,pk):
    if request.is_ajax and request.method == "POST":
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        mobile_no = request.POST['mobileno']

        instance = User.objects.get(pk=pk)
        instance.first_name = firstname
        instance.last_name = lastname
        instance.mobile_no = mobile_no
        instance.save()
        return JsonResponse({
            'first_name': instance.first_name, 
            'last_name': instance.last_name,
            'mobile_no': instance.mobile_no
            }, status=200)
    return JsonResponse({'message': 'Operation failed'}, status=400)


@login_required(login_url='login')
def home(request):
    schools_count = School.objects.count()
    context = {
        'dashboard': "active",
        'school_count': schools_count
    }
    return render(request, 'student_parents/index1.html', context=context)


# <<<<<<<<<< JsonCall view >>>>>>>>>>
def jsoncall(request):
    state = 'Maharashtra'
    districts = []
    data =  json.load(open("static/states-and-districts.json"))
    for i in data:
        if i["state"] == state:
            a = i["districts"]
            print(a)
            districts.append(a)
    return JsonResponse(districts, safe=False)

import uuid 




@login_required(login_url='login')
def Registerchild(request):
    studentform = StudentFrom()
    additionalform = AdditionalDetailsFrom()

    print('here')

    if request.method == 'POST':
        form1 = StudentFrom(request.POST or None)
        form2 = AdditionalDetailsFrom(request.POST or None)

        #unique key is generate here for user
        uninque_key = uuid.uuid4().hex[:6].upper()
        print('-------------------------------------')
        print(uninque_key)

        if form1.is_valid():
            
            # firstname = studentform.cleaned_data['firstname']
            # lastname = studentform.cleaned_data['lastname']
            # gender = studentform.cleaned_data['gender']
            # DOB = studentform.cleaned_data['DOB']
            # admission_Number = studentform.cleaned_data['admission_Number']
            # religion = studentform.cleaned_data['religion']
            # caste = studentform.cleaned_data['caste']
            # aadhar = studentform.cleaned_data['aadhar']
            instance = form1.save(commit=False)
            instance.student_id = uninque_key
            instance.user = request.user
            instance.save()

            # student = Student(
            #     student_id=uninque_key,
            #     user=request.user,
            #     firstname=firstname,
            #     lastname=lastname,
            #     gender=gender,
            #     DOB=DOB,
            #     admission_Number=admission_Number,
            #     religion=religion,
            #     caste=caste,
            #     aadhar=aadhar)
                
            # student.save()

        if additionalform.is_valid():
            # privious_school = additionalform.cleaned_data['privious_school']
            # transfer_certificate_no = additionalform.cleaned_data['transfer_certificate_no']
            # fee_waiver_category = additionalform.cleaned_data['fee_waiver_category']
            # route_code = additionalform.cleaned_data['route_code']
            # shift = additionalform.cleaned_data['shift']
            # stoppage_name = additionalform.cleaned_data['stoppage_name']

            # additional = AdditionalDetails(
            #     student_id=uninque_key,
            #     user=request.user,
            #     privious_school=privious_school,
            #     transfer_certificate_no=transfer_certificate_no,
            #     fee_waiver_category=fee_waiver_category,
            #     route_code=route_code,
            #     shift=shift,
            #     stoppage_name=stoppage_name,
            # )
            # additional.save()
            instance = form1.save(commit=False)
            instance.student_id = uninque_key
            instance.user = request.user
            instance.save()

        return redirect('register_child')

    student_list = Student.objects.filter(user = request.user)
    context = {
        'studentform': studentform,
        'additionalform': additionalform,
        'student_list' : student_list,
    }

    return render(request, 'student_parents/student_add.html', context=context)


@login_required(login_url='login')
def RegisterStudent(request):
    
    error = []
    studentform = StudentFrom()
    contactform = ContactDetailsFrom()
    parentform = ParentDetailsFrom()
    additionalform = AdditionalDetailsFrom()
    documentsform = DocumentsFrom()
    if request.method == 'POST':
        studentform = StudentFrom(request.POST or None)
        contactform = ContactDetailsFrom(
            request.POST or None)
        parentform = ParentDetailsFrom(
            request.POST or None)
        additionalform = AdditionalDetailsFrom(
            request.POST or None)
        documentsform = DocumentsFrom(
            request.POST or None, request.FILES)

        #unique key is generate here for user
        uninque_key = uuid.uuid4().hex[:6].upper()
        print('-------------------------------------')
        print(uninque_key)

        if studentform.is_valid():
            
            # firstname = studentform.cleaned_data['firstname']
            # lastname = studentform.cleaned_data['lastname']
            # gender = studentform.cleaned_data['gender']
            # DOB = studentform.cleaned_data['DOB']
            # admission_Number = studentform.cleaned_data['admission_Number']
            # religion = studentform.cleaned_data['religion']
            # caste = studentform.cleaned_data['caste']
            # aadhar = studentform.cleaned_data['aadhar']
            # student = Student(
            #     student_id=uninque_key,
            #     user=request.user,
            #     firstname=firstname,
            #     lastname=lastname,
            #     gender=gender,
            #     DOB=DOB,
            #     admission_Number=admission_Number,
            #     religion=religion,
            #     caste=caste,
            #     aadhar=aadhar)
                
            instance = studentform.save(commit=False)
            instance.student_id = uninque_key
            instance.user=request.user
            instance.save()
        if contactform.is_valid():
            # current_addr = contactform.cleaned_data['current_addr']
            # current_addr2 = contactform.cleaned_data['current_addr2']
            # state = contactform.cleaned_data['state']
            # city = contactform.cleaned_data['city']
            # pincode = contactform.cleaned_data['pincode']
            # permanent_addr = contactform.cleaned_data['permanent_addr']
            # permanent_addr2 = contactform.cleaned_data['permanent_addr2']
            # permanent_state = contactform.cleaned_data['permanent_state']
            # permanent_city = contactform.cleaned_data['permanent_city']
            # permanent_pincode = contactform.cleaned_data['permanent_pincode']
            # contact = ContactDetails(
            #     student_id=uninque_key,
            #     user=request.user,
            #     current_addr=current_addr,
            #     current_addr2=current_addr2,
            #     state=state,
            #     city=city,
            #     pincode=pincode,
            #     permanent_addr=permanent_addr,
            #     permanent_addr2=permanent_addr2,
            #     permanent_state=permanent_state,
            #     permanent_city=permanent_city,
            #     permanent_pincode=permanent_pincode,
            # )
            instance = contactform.save(commit=False)
            instance.user=request.user
            instance.save()
        if parentform.is_valid():
            # father_name = parentform.cleaned_data['father_name']
            # mother_name = parentform.cleaned_data['mother_name']
            # father_dob = parentform.cleaned_data['father_dob']
            # mother_dob = parentform.cleaned_data['mother_dob']
            # phone_no = parentform.cleaned_data['phone_no']
            # alternate_phone_no = parentform.cleaned_data['alternate_phone_no']
            # email = parentform.cleaned_data['email']
            # father_quali = parentform.cleaned_data['father_quali']
            # mother_quali = parentform.cleaned_data['mother_quali']
            # family_annual_income = parentform.cleaned_data['family_annual_income']
            # parent = ParentDetails(
            #     student_id=uninque_key,
            #     user=request.user,
            #     father_name=father_name,
            #     mother_name=mother_name,
            #     father_dob=father_dob,
            #     mother_dob=mother_dob,
            #     phone_no=phone_no,
            #     alternate_phone_no=alternate_phone_no,
            #     email=email,
            #     father_quali=father_quali,
            #     mother_quali=mother_quali,
            #     family_annual_income=family_annual_income,
            # )
            instance = parentform.save(commit=False)
            instance.user=request.user
            instance.save()
        if additionalform.is_valid():
            # privious_school = additionalform.cleaned_data['privious_school']
            # transfer_certificate_no = additionalform.cleaned_data['transfer_certificate_no']
            # fee_waiver_category = additionalform.cleaned_data['fee_waiver_category']
            # route_code = additionalform.cleaned_data['route_code']
            # shift = additionalform.cleaned_data['shift']
            # stoppage_name = additionalform.cleaned_data['stoppage_name']

            # additional = AdditionalDetails(
            #     student_id=uninque_key,
            #     user=request.user,
            #     privious_school=privious_school,
            #     transfer_certificate_no=transfer_certificate_no,
            #     fee_waiver_category=fee_waiver_category,
            #     route_code=route_code,
            #     shift=shift,
            #     stoppage_name=stoppage_name,
            # )
            instance = additionalform.save(commit=False)
            instance.student_id = uninque_key
            instance.user=request.user
            instance.save()
        if documentsform.is_valid():
            # photo = documentsform.cleaned_data['photo']
            # id_proof = documentsform.cleaned_data['id_proof']
            # caste_certificate = documentsform.cleaned_data['caste_certificate']
            # domicile = documentsform.cleaned_data['domicile']
            # transfer_certificate = documentsform.cleaned_data['transfer_certificate']
            # character_certificate = documentsform.cleaned_data['character_certificate']

            # document = Documents(
            #     student_id=uninque_key,
            #     user=request.user,
            #     photo=photo,
            #     id_proof=id_proof,
            #     caste_certificate=caste_certificate,
            #     domicile=domicile,
            #     transfer_certificate=transfer_certificate,
            #     character_certificate=character_certificate,
            # )
            instance = documentsform.save(commit=False)
            instance.user=request.user
            instance.save()

        student_list = Student.objects.filter(user = request.user)
        context = {
            'student_list' : student_list,
            'register_student': "active"
        }

        return render(request, 'student_parents/student_add.html', context=context)
        
    student_list = Student.objects.filter(user = request.user)
    context = {
        'studentform': studentform,
        'contactform': contactform,
        'parentform': parentform,
        'additionalform': additionalform,
        'documentsform': documentsform,
        'errors': error,
        'student_list' : student_list,
        'register_student': "active",
    }

    return render(request, 'student_parents/student_add.html', context=context)


@login_required(login_url='login')
def detail_view(request, student_id):
    user = request.user
    student = get_object_or_404(Student, user=user, student_id = student_id)
    contact = get_object_or_404(ContactDetails, user=user)
    parent = get_object_or_404(ParentDetails, user=user)
    additional = get_object_or_404(AdditionalDetails, user=user, student_id = student_id)
    documents = get_object_or_404(Documents, user=user)

    studentform = StudentFrom(request.POST or None, instance=student)
    contactform = ContactDetailsFrom(request.POST or None, instance=contact)
    parentform = ParentDetailsFrom(request.POST or None, instance=parent)
    additionalform = AdditionalDetailsFrom(
        request.POST or None, instance=additional)
    documentsform = DocumentsFrom(
        request.POST, request.FILES, instance=documents)

    context = {
        'studentform': studentform,
        'contactform': contactform,
        'parentform': parentform,
        'additionalform': additionalform,
        'documentsform': documentsform,
        'student_id' : student_id
        
    }

    return render(request, 'student_parents/student_edit.html', context=context)


@login_required(login_url='login')
def UpdateRegisterStudent(request, student_id):
    error = []
    user = request.user
    a = student = get_object_or_404(Student, user=user, student_id=student_id)
    print(a)
    contact = get_object_or_404(ContactDetails, user=user)
    parent = get_object_or_404(ParentDetails, user=user)
    additional = get_object_or_404(AdditionalDetails, user=user,  student_id=student_id)
    documents = get_object_or_404(Documents, user=user)

    studentform = StudentFrom(instance=student)
    contactform = ContactDetailsFrom(instance=contact)
    parentform = ParentDetailsFrom(instance=parent)
    additionalform = AdditionalDetailsFrom(instance=additional)
    documentsform = DocumentsFrom(instance=documents)

    if request.method == 'POST':
    
        studentform = StudentFrom(request.POST or None, instance=student)
        contactform = ContactDetailsFrom(request.POST or None, instance=contact)
        parentform = ParentDetailsFrom(request.POST or None, instance=parent)
        additionalform = AdditionalDetailsFrom(
            request.POST or None, instance=additional)
        documentsform = DocumentsFrom(
            request.POST, request.FILES, instance=documents)

        if studentform.is_valid():
            studentform.save()
        else:
            print(studentform.errors)
            error.append("something wrong in Student detail")

        if contactform.is_valid():
            contactform.save()
        else:
            error.append("something wrong in Contact detail")

        if parentform.is_valid():
            parentform.save()
        else:
            error.append("something wrong in Parent detail")

        if additionalform.is_valid():
            additionalform.save()
        else:
            error.append("something wrong in Additional detail")

        if documentsform.is_valid():
            documentsform.save()
        else:
            error.append("something wrong in Documents")

        for i in error:
            print(i)

    context = {
        'studentform': studentform,
        'contactform': contactform,
        'parentform': parentform,
        'additionalform': additionalform,
        'documentsform': documentsform,
        'errors': error,
    }

    return render(request, 'student_parents/student_edit.html', context=context)


def Delete(request, student_id):
    
    student = get_object_or_404(Student, user=request.user, student_id=student_id)
    student.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def school_dashboard(request):
    school_instance = School.objects.get(pk=147)
    
    context = {
        'school_dashboard': True
    }
    return render(request, 'school/school_dashboard.html', context)
