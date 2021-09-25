from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

import os, csv
User = settings.AUTH_USER_MODEL

class School(models.Model):

    CLASS_OFFERED_CHOISES = [
        ('Nursery - Class 12', 'Nursery - Class 12'),
        ('Nursery - Class 10', 'Nursery - Class 10'),
        ('Toddler - Class 12', 'Toddler - Class 12'),
        ('Pre-Nursery - Class 5', 'Pre-Nursery - Class 5'),
        ('Pre-Nursery - Class 8', 'Pre-Nursery - Class 8'),
        ('Nursery - Class 8', 'Nursery - Class 8'),
        ('Class 1 - Class 12', 'Class 1 - Class 12'),
        ('Pre-Nursery - Class 12', 'Pre-Nursery - Class 12'),
        ('Pre-Nursery - KG', 'Pre-Nursery - KG'),
        ('Nursery - UKG', 'Nursery - UKG'),
        ('Pre-Nursery - Class 10', 'Pre-Nursery - Class 10'),
        ('Class 6 - Class 12', 'Class 6 - Class 12'),
        ('Class 1 - Class 8', 'Class 1 - Class 8'),
        ('Pre-Nursery - UKG', 'Pre-Nursery - UKG'),
        ('Nursery - KG', 'Nursery - KG'),
        ('Pre-School (Nursery) - Class 12', 'Pre-School (Nursery) - Class 12'),
        ('LKG - Class 12', 'LKG - Class 12'),
        ('Nursery - Class 3', 'Nursery - Class 3'),
        ('Pre-Nursery - Class 7', 'Pre-Nursery - Class 7'),
        ('Play Group - Class 1', 'Play Group - Class 1'),
        ('Nursery - Class 11', 'Nursery - Class 11'),
        ('Nursery - Class 7', 'Nursery - Class 7'),
        ('Nursery - Class 9', 'Nursery - Class 9'),
        ('Pre-School (Nursery) - Class 5', 'Pre-School (Nursery) - Class 5'),
        ('LKG - Class 10', 'LKG - Class 10'),
        ('Pre-School (Nursery) - Class 10', 'Pre-School (Nursery) - Class 10'),
        ('Pre-Nursery - Class 2', 'Pre-Nursery - Class 2'),
        ('Pre-Nursery - Prep', 'Pre-Nursery - Prep'),
        ('KG - Class 12', 'KG - Class 12'),
        ('Pre-School (Nursery) - Class 1', 'Pre-School (Nursery) - Class 1'),
        ('Nursery - Class 5', 'Nursery - Class 5'),
        ('LKG - Class 9', 'LKG - Class 9'),
        ('Nursery - Class 2', 'Nursery - Class 2'),
        ('UKG - Class 12', 'UKG - Class 12'),
        ('Class 1 - Class 11', 'Class 1 - Class 11'),
        ('Play Way - Class 12', 'Play Way - Class 12'),
        ('Pre-School (Nursery) - Pre-Primary (KG)', 'Pre-School (Nursery) - Pre-Primary (KG)'),
        ('Play Group - UKG', 'Play Group - UKG'),
        ('Pre-Nursery - Class 6', 'Pre-Nursery - Class 6'),
        ('UKG - Class 4', 'UKG - Class 4'),
        ('KG - Class 10', 'KG - Class 10'),
        ('Play Way - Class 10', 'Play Way - Class 10'),
        ('KG - Class 8', 'KG - Class 8'),
        ('Play School - Class 8', 'Play School - Class 8'),
        ('Class 1 - Class 5', 'Class 1 - Class 5'),
        ('Pre-Nursery - Class 9', 'Pre-Nursery - Class 9'),
        ('Class 6 - Class 10', 'Class 6 - Class 10'),
        ('Play Group - Class 5', 'Play Group - Class 5'),
        ('Nursery - Class 1', 'Nursery - Class 1'),
        ('Nursery - Class 6', 'Nursery - Class 6'),
        ('Pre-Nursery - Class 3', 'Pre-Nursery - Class 3'),
        ('Class 3 - Class 12', 'Class 3 - Class 12'),
        ('Class 1 - Class 10', 'Class 1 - Class 10'),
        ('Class 6 - Class 8', 'Class 6 - Class 8'),
        ('UKG - Class 10', 'UKG - Class 10'),
        ('Class 1 - Class 6', 'Class 1 - Class 6'),
        ('LKG - Class 8', 'LKG - Class 8'),
        ('Pre-Nursery - Nursery', 'Pre-Nursery - Nursery'),
        ('UKG - Class 5', 'UKG - Class 5'),
        ('Class 1 - Class 7', 'Class 1 - Class 7'),
        ('LKG - Class 5', 'LKG - Class 5'),
        ('Class 9 - Class 12', 'Class 9 - Class 12'),
        ('Play Group - Class 8', 'Play Group - Class 8'),
        ('Play Group - Class 10', 'Play Group - Class 10'),
        ('UKG - Class 8', 'UKG - Class 8'),
    ]

    UNKWON_TYPE = 'UN'
    OWNERSHIP_TYPE_CHOICES = [
        (UNKWON_TYPE, 'UNKNOWN'),
        ('PR', 'PRIVATE'),
        ('PRA', 'PRIVATE-AIDED'),
    ]  

    STATE_BOARD = 'SB'
    BOARD_TYPE_CHOICES = [
        (STATE_BOARD, 'STATE BOARD'),
        ('CBSE', 'CBSE'),
        ('ICSE', 'ICSE'),
        ('CISCE', 'CISCE'),
        ('NIOS', 'NIOS'),
        ('IB', 'IB'),
        ('CIE', 'CIE'),
    ]

    CO_ED_CHOICES = [
        ('Co-Education', 'Co-Education'), 
        ('Girlsonly', 'Girlsonly'), 
        ('Boysonly', 'Boysonly')
    ]

    owner = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null = True)
    school_name = models.CharField(max_length=500)
    school_image = models.CharField(max_length=999, blank=True)
    address = models.TextField(max_length=250)
    board = models.CharField(max_length=5, choices=BOARD_TYPE_CHOICES, default=STATE_BOARD)
    co_ed_status = models.CharField(max_length=100, choices=CO_ED_CHOICES)
    ownership = models.CharField(max_length=3, choices=OWNERSHIP_TYPE_CHOICES, default=UNKWON_TYPE)
    sf_ratio = models.CharField(max_length=6)
    class_offered = models.CharField(max_length=100, choices=CLASS_OFFERED_CHOISES)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.school_name}"


class SchoolDetail(models.Model):
    school = models.ForeignKey(School, related_name='school', on_delete=models.CASCADE)
    phone_no = models.CharField(max_length=500)
    webiste = models.CharField(max_length=500)
    email = models.CharField(max_length=500)
    year_of_establishment = models.CharField(max_length=500)
    campus_size = models.CharField(max_length=500)
    campus_type = models.CharField(max_length=500)
    gallery = models.CharField(max_length=99999)

    def __str__(self):
        return f"{self.school.school_name}"


class SchoolFacilities(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    #class
    ac_classes = models.BooleanField(default=False)
    smart_classes = models.BooleanField(default=False)
    wifi = models.BooleanField(default=False)
    #boarding
    boys_hostel = models.BooleanField(default=False)
    girls_hostel = models.BooleanField(default=False)
    #infrastructure
    auditorium_media_room = models.BooleanField(default=False)
    cafeteria_canteen = models.BooleanField(default=False)
    library_reading_room = models.BooleanField(default=False)
    playground = models.BooleanField(default=False)
    #safty and security
    cctv = models.BooleanField(default=False)
    gps_bus_tracking_app = models.BooleanField(default=False)
    student_tracking_app = models.BooleanField(default=False)
    #advanced facilities
    alumni_association = models.BooleanField(default=False)
    day_care = models.BooleanField(default=False)
    meals = models.BooleanField(default=False)
    medical_room = models.BooleanField(default=False)
    transportation = models.BooleanField(default=False)
    #extra curricular
    art_and_craft = models.BooleanField(default=False)
    dance = models.BooleanField(default=False)
    debate = models.BooleanField(default=False)
    drama = models.BooleanField(default=False)
    gardening = models.BooleanField(default=False)
    music = models.BooleanField(default=False)
    picnics_and_excursion = models.BooleanField(default=False)
    # sports and fitness
    skating = models.BooleanField(default=False)
    horse_riding = models.BooleanField(default=False)
    gym = models.BooleanField(default=False)
    indoor_sports = models.BooleanField(default=False)
    outdoor_sports = models.BooleanField(default=False)
    swimming_pool = models.BooleanField(default=False)
    karate = models.BooleanField(default=False)
    taekwondo = models.BooleanField(default=False)
    yoga = models.BooleanField(default=False)
    # lab
    computer_lab = models.BooleanField(default=False)
    science_lab = models.BooleanField(default=False)
    robotics_lab = models.BooleanField(default=False)
    # disabled friendly
    ramps = models.BooleanField(default=False)
    washrooms = models.BooleanField(default=False)
    elevators = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.school.school_name}"
    
    class Meta:
        verbose_name_plural = "School Facilities"


class HallofFame(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.school.school_name}"

class SchoolReviews(models.Model):
    rating = models.IntegerField(default=0, validators=[MinValueValidator(0),MaxValueValidator(5)])
    comment = models.CharField(max_length=999)
    school = models.ForeignKey(SchoolDetail, related_name='school_reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    created_at =models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user}"

    class Meta:
        verbose_name_plural = "School Reviews"


class SchoolFee(models.Model):
    school = models.ForeignKey(School, related_name='school_refer', on_delete=models.CASCADE)
    fee_name = models.CharField(max_length=50)
    fee_amount = models.IntegerField()
    standard = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.school.school_name}"

class SchoolRegistration(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    email = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255, )
    contact_number = models.CharField(max_length=14)
    school = models.ForeignKey(School , on_delete=models.CASCADE)


class SchoolGallery(models.Model):
    school = models.ForeignKey(School , on_delete=models.CASCADE)
    school_img = models.ImageField(upload_to='images/')

    def __str__(self):
        return f"{self.school.school_name}"