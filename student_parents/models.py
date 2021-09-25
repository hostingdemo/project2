from django.db import models


from django.conf import settings
User = settings.AUTH_USER_MODEL


# Create your models here.


# <<<<<<<<<< Student >>>>>>>>>>>>
Gender = [('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]


class Student(models.Model):
    student_id = models.CharField(max_length=100, null=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    firstname = models.CharField(max_length=100, null=True)
    lastname = models.CharField(max_length=100, null=True)
    gender = models.CharField(max_length=100, choices=Gender, default='Male')
    DOB = models.DateField(auto_now=False, auto_now_add=False, null=True)
    admission_Number = models.CharField(max_length=12, null=True)
    religion = models.CharField(max_length=100, null=True, blank=True)
    caste = models.CharField(max_length=100, null=True, blank=True)
    aadhar = models.CharField(max_length=12, null=True)
    create_at = models.DateTimeField(auto_now_add=True)


# <<<<<<<<<< ContactDetailsForm >>>>>>>>>>>>
class ContactDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    current_addr = models.CharField(max_length=100, null=True)
    current_addr2 = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    pincode = models.CharField(max_length=10, default='00000', null=True)
    # <<<<<Permanent Address>>>>>
    permanent_addr = models.CharField(max_length=100, null=True, blank=True)
    permanent_addr2 = models.CharField(max_length=100, null=True, blank=True)
    permanent_state = models.CharField(max_length=100, null=True, blank=True)
    permanent_city = models.CharField(max_length=100, null=True, blank=True)
    permanent_pincode = models.CharField(
        max_length=10, default='00000', null=True)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}"

    class Meta:
        verbose_name_plural = f"Contact Details"


# <<<<<<<<<< ParentDetails >>>>>>>>>>>>
class ParentDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    father_name = models.CharField(max_length=100, null=True)
    mother_name = models.CharField(max_length=100, null=True)
    father_dob = models.DateField(
        auto_now=False, auto_now_add=False, null=True, blank=True)
    mother_dob = models.DateField(
        auto_now=False, auto_now_add=False, null=True, blank=True)
    phone_no = models.CharField(max_length=15, null=True, blank=True)
    alternate_phone_no = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    father_quali = models.CharField(max_length=100, blank=True, null=True)
    mother_quali = models.CharField(max_length=100, blank=True, null=True)
    family_annual_income = models.IntegerField(default=0)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}"

    class Meta:
        verbose_name_plural = f"Parent Details"


# <<<<<<<<<< AdditionalDetailz >>>>>>>>>>>>
class AdditionalDetails(models.Model):
    student_id = models.CharField(max_length=100, null=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    privious_school = models.CharField(max_length=100, blank=True, null=True)
    transfer_certificate_no = models.CharField(
        max_length=100, blank=True, null=True)
    fee_waiver_category = models.CharField(
        max_length=100, blank=True, null=True)
    route_code = models.CharField(max_length=100, blank=True, null=True)
    shift = models.CharField(max_length=100, blank=True, null=True)
    stoppage_name = models.CharField(max_length=100, blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}"

    class Meta:
        verbose_name_plural = f"Additional Details"


# <<<<<<<<<< Documents >>>>>>>>>>>>
class Documents(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    photo = models.FileField(upload_to="media", default='shri.jpg', null=True)
    id_proof = models.FileField(upload_to="media", null=True, blank=True)
    caste_certificate = models.FileField(
        upload_to="media", blank=True, null=True)
    domicile = models.FileField(upload_to="media", blank=True, null=True)
    transfer_certificate = models.FileField(
        upload_to="media", blank=True, null=True)
    character_certificate = models.FileField(
        upload_to="media", blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}"

    class Meta:
        verbose_name_plural = f"Documents"
