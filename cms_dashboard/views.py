from django.core.paginator import Paginator
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import View
from django.contrib import messages
import csv, io, ast
from schools.models import *
from django.core import serializers

from schools.forms import *

from schools.models import HallofFame, School, SchoolDetail, SchoolFacilities


class CmsDashboard(View):
    def get(self, request):
        return render(request, 'cms_dashboard/index1.html', {'dashboard': 'active'})


class UploadCsv(View):
    template_name = 'cms_dashboard/upload-csv.html'
    def get(self, request):
        school_list = School.objects.all().order_by('school_name')
        paginator = Paginator(school_list, 25)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, self.template_name, {'page_obj': page_obj})

    def post(self, request):
        csv_file = request.FILES['csv-file']
        # let's check if it is a csv file
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'THIS IS NOT A CSV FILE')
        data_set = csv_file.read().decode('UTF-8')
        # setup a stream which is when we loop through each line we are able to handle a data in a stream
        io_string = io.StringIO(data_set)
        reader = csv.DictReader(io_string)
        try:
            for row in reader:
                #school
                ownership=row['Ownership']
                school_name=row['school_name']
                school_image=row['school_image']
                board=row['Board']
                address=row['address']
                co_ed_status=row['Co-Ed Status']
                class_offered=row['class_offered']
                sf_ratio=row['sf_ratio']


                #school details
                gallery=row['gallery']
                email=row['email']
                website=row['website']
                phone_no=row['phone_no']
                year_of_establishment=row['Year of Establishment']
                campus_size=row['Campus Size']
                campus_type=row['Campus Type']

                #school facilities
                ac_classes=row['ac_classes']
                smart_classes=row['smart_classes']
                wifi=row['wifi']
                boys_hostel=row['boys_hostel']
                girls_hostel=row['girls_hostel']
                auditorium_media_room=row['auditorium/media_room']
                cafeteria_canteen=row['cafeteria/canteen']
                library_reading_room=row['library/reading_room']
                playground=row['playground']
                cctv=row['cctv']
                gps_bus_tracking_app=row['gps_bus_tracking_app']
                student_tracking_app=row['student_tracking_app']
                alumni_association=row['alumni_association']
                day_care=row['day_care']
                meals=row['meals']
                medical_room=row['medical_room']
                transportation=row['transportation']
                art_and_craft=row['art_and_craft']
                dance=row['dance']
                debate=row['debate']
                drama=row['drama']
                gardening=row['gardening']
                music=row['music']
                picnics_and_excursion=row['picnics_and_excursion']
                skating=row['skating']
                horse_riding=row['horse_riding']
                gym=row['gym']
                indoor_sports=row['indoor_sports']
                outdoor_sports=row['outdoor_sports']
                swimming_pool=row['swimming_pool']
                karate=row['karate']
                taekwondo=row['taekwondo']
                yoga=row['yoga']
                computer_lab=row['computer_lab']
                science_lab=row['science_lab']
                robotics_lab=row['robotics_lab']
                ramps=row['ramps']
                washrooms=row['washrooms']
                elevators=row['elevators']
                hall_of_fame=row['hall_of_fame']
                

                ## Creating school instances
                school_obj, created1 = School.objects.update_or_create(
                    school_name=school_name,
                    address=address,
                    board=board,
                    co_ed_status=co_ed_status,
                    ownership=ownership,
                    school_image=school_image,
                    sf_ratio=sf_ratio,
                    class_offered=class_offered
                )

                ## Creating school details instances
                school_detail_obj, created2 = SchoolDetail.objects.update_or_create(
                    school = school_obj,
                    phone_no = phone_no,
                    webiste = website,
                    email = email,
                    year_of_establishment = year_of_establishment,
                    campus_size = campus_size,
                    campus_type = campus_type,
                    gallery = gallery,
                )
            
                ## Creating school facilities instances
                school_fc_obj, created3 = SchoolFacilities.objects.update_or_create(
                    school = school_obj,
                    #class
                    ac_classes = ac_classes,  
                    smart_classes = smart_classes,  
                    wifi = wifi,  
                    #boarding
                    boys_hostel = boys_hostel,  
                    girls_hostel = girls_hostel,  
                    #infrastructure
                    auditorium_media_room = auditorium_media_room,  
                    cafeteria_canteen = cafeteria_canteen,  
                    library_reading_room = library_reading_room,  
                    playground = playground,  
                    #safty and security
                    cctv = cctv,  
                    gps_bus_tracking_app = gps_bus_tracking_app,  
                    student_tracking_app = student_tracking_app,  
                    #advanced facilities
                    alumni_association = alumni_association,  
                    day_care = day_care,  
                    meals = meals,  
                    medical_room = medical_room,  
                    transportation = transportation,  
                    #extra curricular
                    art_and_craft = art_and_craft,  
                    dance = dance,  
                    debate = debate,  
                    drama = drama,  
                    gardening = gardening,  
                    music = music,  
                    picnics_and_excursion = picnics_and_excursion,  
                    # sports and fitness
                    skating =   skating,  
                    horse_riding = horse_riding,  
                    gym = gym,  
                    indoor_sports = indoor_sports,  
                    outdoor_sports = outdoor_sports,  
                    swimming_pool = swimming_pool,  
                    karate = karate,  
                    taekwondo = taekwondo,  
                    yoga = yoga,  
                    # lab
                    computer_lab = computer_lab,  
                    science_lab = science_lab,  
                    robotics_lab = robotics_lab,  
                    # disabled friendly
                    ramps = ramps,  
                    washrooms = washrooms,  
                    elevators = elevators, 
                ) 

                ## Creating hall of fame instances
                hof_list = ast.literal_eval(hall_of_fame)
                if(len(hof_list)>0):
                    for h in hof_list:
                        hall_of_fame_obj, created4 = HallofFame.objects.update_or_create(
                            school = school_obj,
                            title=h
                        )
                print(row['school_name'])
        except Exception as e:
            print(e)
        return redirect('upload_csv')




def employee_school_info(request, school_id):
   
    if request.method == 'POST':
        instance = School.objects.get(id=school_id)
        form = school_addForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            instance = School.objects.get(id=school_id)
            form = school_addForm(instance=instance)
            fee_data = SchoolFee.objects.filter(school=instance)
            return render(request, 'employee/school_form.html', {'school_form': form, 'instance': instance, 'fee_data': fee_data, 'School_Information' : 'active'})
    else:
      
        instance = School.objects.get(id=school_id)
        fee_data = SchoolFee.objects.filter(school=instance)
        form = school_addForm(instance=instance)
        return render(request, 'employee/school_form.html', {'school_form': form, 'instance': instance, 'fee_data': fee_data})
    

    
def school_facilities(request, school_id):
    if request.method == 'POST':
      
        instance = School.objects.get(id=school_id)
        form = school_fc_Form(request.POST)
        if form.is_valid():
            return redirect('employee_school_facilities')
      
    else:
      
        instance = School.objects.get(id=school_id)
        school_facilities = SchoolFacilities.objects.get(school=instance)
        form = school_fc_Form(instance=school_facilities)
        return render(request, 'employee/school_facilities.html', {'school_fc_form': form, 'instance':instance, 'employee_school_facilities': 'active'})
    
class SchoolFeesView(View):
    def get(self, request, *args, **kwargs ):
        school_id = self.kwargs['school_id']
        
        school_instance = School.objects.get(id=school_id)

        print(school_instance)
        
        school_fee_instance = SchoolFee.objects.filter(school=school_instance)
        serialized_data = serializers.serialize('json', school_fee_instance)
        return JsonResponse({'data': serialized_data}, status=200)
    
        
    def post(self, request, *args, **kwargs):
        print('in post')
        standard = request.POST.get('standard')
        fee_name = request.POST.get('fee-name')
        fee_amount = request.POST.get('fee-amount')
        school_id = request.POST.get('school_id')
        fee_id = request.POST.get('fee-id')
        try:
            school_instance = School.objects.get(id=school_id)
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
      
        SchoolFee.objects.get(pk=_id).delete()
        return JsonResponse({'message': 'Deleted successfully'}, status=201)
    

## Hall of fame
class SchoolFameView(View ):
    def get(self, request, school_id):
    
        instance = School.objects.get(id=school_id)
        return render(request, "employee/hall_of_fame.html", {'instance':instance, 'employee_school_fame': 'active'})
    
class HallofFameAdd(View):
    def get(self, request, school_id):
        
        school_instance = School.objects.get(id=school_id)
        instance = HallofFame.objects.filter(school=school_instance)
        sr_data = serializers.serialize('json', instance)
        return JsonResponse({'data': sr_data}, status=200)
    
    def post(self, request, school_id):
        fame_title = request.POST.get('fame-title')
        fame_id = request.POST.get('fame-id')
        try:
            school_instance = School.objects.get(id=school_id)
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
      
        HallofFame.objects.get(pk=_id).delete()
        return JsonResponse({'message': 'Deleted successfully'}, status=201)
    
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

       
