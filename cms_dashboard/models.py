from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.db import models

import csv, os, ast

from schools.models import HallofFame, School, SchoolDetail, SchoolFacilities

#===#
class CSVFile(models.Model):
    csv_file = models.FileField(max_length=999, upload_to="csv_files", blank=False, null=False)
    upload_date = models.DateTimeField(auto_now_add=True)
        
    def __str__(self):
        return f"{self.csv_file}"
    



# post save signal
@receiver(post_save, sender=CSVFile, dispatch_uid="add_records_to_schools_from_csv_file")
def add_records_to_schools_from_csv_file(sender, instance, **kwargs):
    to_import = os.path.join(settings.MEDIA_ROOT, instance.csv_file.name)
    print('-'*10)
    print(to_import)
    print('-'*10)

    with open(to_import) as f:
        reader = csv.DictReader(f)
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