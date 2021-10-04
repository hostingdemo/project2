from django.db import models
from django.core.validators import ValidationError

from django.conf import settings
User = settings.AUTH_USER_MODEL


class Child(models.Model):
    GENDER = [
        ('N', 'Dosn\'t Want to Specify'),
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    CLASS_STANDARD = [
        ('UKG', 'UKG'),
        ('LKG', 'LKG'),
        ('PLG', 'Play Group'),
        ('NRS', 'Narsery'),
        ('1', 'Class 1'),
        ('2', 'Class 2'),
        ('3', 'Class 3'),
        ('4', 'Class 4'),
        ('5', 'Class 5'),
        ('6', 'Class 6'),
        ('7', 'Class 7'),
        ('8', 'Class 8'),
        ('9', 'Class 9'),
        ('10', 'Class 10'),
        ('11', 'Class 11'),
        ('12', 'Class 12'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class_standard = models.CharField(max_length=3, choices=CLASS_STANDARD)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(auto_now=False, auto_now_add=False)
    gender = models.CharField(max_length=1, choices=GENDER, default="N")

    def __str__(self):
        return f"{self.user.email} - {self.first_name} {self.last_name}"

    class Meta:
        verbose_name_plural = f"Child"


# <<<<<<<<<< child Info >>>>>>>>>>>>
class CommonForm(models.Model):

    RELIGION_CHOICES = [
        ('hinduism','Hinduism'),
        ('sikhism','Sikhism'),
        ('islam', 'Islam'),
        ('christianity', 'Christianity'),
        ('zoroastrianism', 'Zoroastrianism'),
        ('buddhism', 'Buddhism'),
        ('jainism', 'Jainism'),
    ]

    CATEGORY_CHOICES = [
        ('GENERAL','GENERAL'),
        ('SC','SC'),
        ('ST','ST'),
        ('OBC', 'OBC'),
    ]

    BLOOD_GROUP_CHOICES = [
        ('A+','A+'),
        ('B+','B+'),
        ('AB+','AB+'),
        ('O+', 'O+'),
        ('A-','A-'),
        ('B-','B-'),
        ('AB-','AB-'),
        ('O-', 'O-'),
    ]

    MINORITY_CHOICES = [
        (True, 'Yes'),
        (False, 'No')
    ]

    def validate_digit_length(aadhar):
        if not (aadhar.isdigit() and len(aadhar) == 12):    
            raise ValidationError('must be 12 digits')


    child = models.ForeignKey(Child, on_delete=models.CASCADE, null=True)
    admission_number = models.CharField(max_length=12, null=True)

    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)

    religion = models.CharField(max_length=100, choices=RELIGION_CHOICES)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    minority = models.BooleanField(default=False, choices=MINORITY_CHOICES)
    
    aadhar_no = models.CharField(max_length=12, validators=[validate_digit_length])

    single_child = models.BooleanField(default=False)
    adopted_child = models.BooleanField(default=False)
    orphan_child = models.BooleanField(default=False)
    child_with_needs = models.BooleanField(default=False)

    # <<<<<<<<<< ContactDetailsForm >>>>>>>>>>>>
    current_address_line_1 = models.CharField(max_length=100)
    current_address_line_2 = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)

    # <<<<<Permanent Address>>>>>
    permanent_address_line_1 = models.CharField(max_length=100)
    permanent_address_line_2 = models.CharField(max_length=100, null=True, blank=True)
    permanent_state = models.CharField(max_length=100)
    permanent_city = models.CharField(max_length=100)
    permanent_pincode = models.CharField(max_length=6)
    
    # <<<<<<<<<< ParentDetails >>>>>>>>>>>>
    fathers_name = models.CharField(max_length=100, null=True)
    fathers_dob = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    fathers_qualification = models.CharField(max_length=100, blank=True, null=True)
    mothers_name = models.CharField(max_length=100, null=True)
    mothers_dob = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    mothers_qualification = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    phone_no = models.CharField(max_length=15, null=True, blank=True)
    alternate_phone_no = models.CharField(max_length=15, null=True, blank=True)
    family_annual_income = models.PositiveIntegerField(default=0)

    # <<<<<<<<<< AdditionalDetailz >>>>>>>>>>>>
    privious_school = models.CharField(max_length=100, blank=True, null=True)
    transfer_certificate_no = models.CharField(max_length=100, blank=True, null=True)
    fee_waiver_category = models.CharField( max_length=100, blank=True, null=True)
    route_code = models.CharField(max_length=100, blank=True, null=True)
    shift = models.CharField(max_length=100, blank=True, null=True)
    stoppage_name = models.CharField(max_length=100, blank=True, null=True)

    # <<<<<<<<<< Documents >>>>>>>>>>>>
    photo = models.ImageField(upload_to="documents", null=True, blank=True)
    id_proof = models.FileField(upload_to="documents", null=True, blank=True)
    caste_certificate = models.FileField(upload_to="documents", blank=True, null=True)
    domicile = models.FileField(upload_to="documents", blank=True, null=True)
    transfer_certificate = models.FileField(upload_to="documents", blank=True, null=True)
    character_certificate = models.FileField(upload_to="documents", blank=True, null=True)