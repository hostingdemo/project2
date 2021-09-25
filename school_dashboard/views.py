import json
from django.http import request
from schools.models import School, SchoolFee
from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse
from schools.forms import school_addForm, school_fc_Form
from django.shortcuts import redirect, render
from django.core import serializers
from django.views.generic import View

from schools.models import *

# Create your views here.
def dashboard(request):
    try:
        instance = School.objects.get(owner=request.user)
        data = school_addForm(instance=instance)
        return render(request, 'school_dashboard/index1.html', {'dashboard': 'active', 'data':data})
    except Exception as e:
        print(e)
        return HttpResponse('You are not authorized!')


def school_info(request):
    if request.method == 'POST':
        instance = School.objects.get(owner=request.user)
        form = school_addForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            instance = School.objects.get(owner=request.user)
            form = school_addForm(instance=instance)
            fee_data = SchoolFee.objects.all(school=instance)
            return render(request, 'school_dashboard/school_form.html', {'school_form': form, 'instance': instance, 'fee_data': fee_data})
    else:
        try:
            instance = School.objects.get(owner=request.user)
            fee_data = SchoolFee.objects.filter(school=instance)
            form = school_addForm(instance=instance)
            return render(request, 'school_dashboard/school_form.html', {'school_form': form, 'instance': instance, 'fee_data': fee_data})
        except Exception as e:
            print(e)
            return HttpResponse('You are not authorized!')

    
def school_facilities(request):
    if request.method == 'POST':
        try:
            instance = School.objects.get(owner=request.user)
            form = school_fc_Form(request.POST)
            if form.is_valid():
                return redirect('school_facilities')
        except Exception as e:
            print(e)
            return HttpResponse('You are not authorized!')
    else:
        try:
            instance = School.objects.get(owner=request.user)
            school_facilities = SchoolFacilities.objects.get(school=instance)
            form = school_fc_Form(instance=school_facilities)
            return render(request, 'school_dashboard/school_facilities.html', {'school_fc_form': form})
        except Exception as e:
            print(e)
            return HttpResponse('You are not authorized!')


class SchoolFeesView(View):
    def get(self, request, *args, **kwargs):
        try:
            school_instance = School.objects.get(owner=request.user)
            school_fee_instance = SchoolFee.objects.filter(school=school_instance)
            serialized_data = serializers.serialize('json', school_fee_instance)
            return JsonResponse({'data': serialized_data}, status=200)
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'Server error'}, status=400)
        
    def post(self, request, *args, **kwargs):
        standard = request.POST.get('standard')
        fee_name = request.POST.get('fee-name')
        fee_amount = request.POST.get('fee-amount')
        fee_id = request.POST.get('fee-id')
        try:
            school_instance = School.objects.get(owner=request.user)
            if not fee_id or fee_id == '':
                school_fee_instance = SchoolFee.objects.create(
                    school=school_instance, 
                    standard=standard,
                    fee_name=fee_name, 
                    fee_amount=fee_amount
                )
                d = serializers.serialize('json', [school_fee_instance])
                return JsonResponse({'message': 'Added successfully', 'data': d}, status=201)
            else:
                instance = SchoolFee.objects.get(pk=fee_id)
                instance.fee_name = fee_name
                instance.fee_amount = fee_amount
                instance.save()
                d = serializers.serialize('json', [instance])
                return JsonResponse({'message': 'Updated successfully', 'data': d}, status=201)
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'Server error'}, status=400)


class SchoolFeeDelete(View):
    def post(self, request):
        _id = request.POST.get('id')
        try:
            SchoolFee.objects.get(pk=_id).delete()
            return JsonResponse({'message': 'Deleted successfully'}, status=201)
        except Exception as e:
            return JsonResponse({'message': 'Server error'}, status=400)



## Hall of fame
class SchoolFameView(View):
    def get(self, request):
        try:
            school_instance = School.objects.get(owner=request.user)
            return render(request, "school_dashboard/hall_of_fame.html", {})
        except Exception as e:
            print(e)
            return HttpResponse('You are not authorized!')

class HallofFameAdd(View):
    def get(self, request):
        try:
            school_instance = School.objects.get(owner=request.user)
            instance = HallofFame.objects.filter(school=school_instance)
            sr_data = serializers.serialize('json', instance)
            return JsonResponse({'data': sr_data}, status=200)
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'Server error'}, status=400)

    def post(self, request):
        fame_title = request.POST.get('fame-title')
        fame_id = request.POST.get('fame-id')
        try:
            school_instance = School.objects.get(owner=request.user)
            if not fame_id or fame_id == '':
                school_fame_instance = HallofFame.objects.create(
                    school=school_instance, 
                    title=fame_title, 
                )
                d = serializers.serialize('json', [school_fame_instance])
                return JsonResponse({'message': 'Added successfully', 'data': d}, status=201)
            else:
                instance = HallofFame.objects.get(pk=fame_id)
                instance.title = fame_title
                instance.save()
                d = serializers.serialize('json', [instance])
                return JsonResponse({'message': 'Updated successfully', 'data': d}, status=201)
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'Server error'}, status=400)


class HallofFameDelete(View):
    def post(self, request):
        _id = request.POST.get('id')
        try:
            HallofFame.objects.get(pk=_id).delete()
            return JsonResponse({'message': 'Deleted successfully'}, status=201)
        except Exception as e:
            return JsonResponse({'message': 'Server error'}, status=400)


class SchoolGalleryView(View):
    def get(self, request):
        school_gallery = SchoolGallery.objects.all()
        return render(request, 'school_dashboard/school_gallery.html', {'school_gallery': school_gallery})

    def post(self, request):
        try:
            school_instance = School.objects.get(owner=request.user)
            img = request.FILES['school-img']

            if not img:
                return HttpResponse('img not provied')
            instance = SchoolGallery(school=school_instance, school_img=img)
            instance.save()
            return redirect('school_gallery')
        except Exception as e:
            print(e)
            return HttpResponse('You are not authorized!')


from django.http import HttpResponseForbidden
def delete_img(request, pk):
    if not request.user:
        return HttpResponseForbidden()
    SchoolGallery.objects.get(pk=pk).delete()
    return redirect('school_gallery')

    