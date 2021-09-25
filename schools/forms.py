from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Column, Layout, Field, Row, Submit
from django import forms
from .models import SchoolFacilities, School

class school_addForm(forms.ModelForm):
    class Meta:
        model = School
        exclude = ('owner', 'school_image', 'verified')

    def __init__(self, *args, **kwargs):
        super(school_addForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control-sm'
        
        self.helper = FormHelper()
        self.helper.form_class = "rounded shadow px-4 py-3 d-flex flex-column"
        self.helper.attrs = {"novalidate": ''}
        self.helper.layout = Layout(
            HTML('<h3 class="mt-4 mb-3">School details</h3>'),
            Row(
                Column(Field('board'), css_class='col-12 col-md-2 col-lg-3'),
                Column(Field('school_name'), css_class='col-12 col-md-10 col-lg-9'),
                Column(Field('ownership'), css_class='col-12 col-md-6 col-lg-3'),
                Column(Field('class_offered'), css_class='col-12 col-md-6 col-lg-3'),
                Column(Field('co_ed_status'), css_class='col-12 col-md-6 col-lg-3'),
                Column(Field('sf_ratio'), css_class='col-12 col-md-6 col-lg-3'),
                Column(Field('address', rows=2), css_class='col-12'),
                css_class='row'
            ),
            Submit('school-form-submit', 'submit', css_class="col-12 col-md-2 btn btn-sm btn-primary")
        )


class school_fc_Form(forms.ModelForm):
    class Meta:
        model = SchoolFacilities
        exclude = ('school',)

    def __init__(self, *args, **kwargs):
        super(school_fc_Form, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_class = "rounded shadow px-4 py-3 d-flex flex-column"
        self.helper.attrs = {"novalidate": ''}
        self.helper.field_class = 'm-0'
        self.helper.layout = Layout(
            HTML('<h3 class="mt-4 mb-3">School Facilities</h3>'),
            Row(
                Column(
                    HTML('<h6 class="text-muted">Classroom</h6>'),
                    'ac_classes',
                    'smart_classes',
                    'wifi',
                    css_class='col-12 col-md-4 col-lg-4 mb-3'
                ),
                Column(
                    HTML('<h6 class="text-muted">Boarding</h6>'),
                    'boys_hostel',
                    'girls_hostel',
                    css_class='col-12 col-md-4 col-lg-4 mb-3'
                ),
                Column(
                    HTML('<h6 class="text-muted">Safty and Security</h6>'),
                    'cctv',
                    'gps_bus_tracking_app',
                    'student_tracking_app',
                    css_class='col-12 col-md-4 col-lg-4 mb-3'
                ),
                Column(
                    HTML('<h6 class="text-muted">Infrastructure</h6>'),
                    'auditorium_media_room',
                    'cafeteria_canteen',
                    'library_reading_room',
                    'playground',
                    css_class='col-12 col-md-4 col-lg-4 mb-3'
                ),
                Column(
                    HTML('<h6 class="text-muted">Labs</h6>'),
                    'computer_lab',
                    'science_lab',
                    'robotics_lab',
                    css_class='col-12 col-md-4 col-lg-4 mb-3'
                ),
                Column(
                    HTML('<h6 class="text-muted">Advanced facilities</h6>'),
                    'alumni_association',
                    'day_care',
                    'meals',
                    'medical_room',
                    'transportation',
                    css_class='col-12 col-md-4 col-lg-4 mb-3'
                ),
                Column(
                    HTML('<h6 class="text-muted">Extra curriculars</h6>'),
                    'art_and_craft',
                    'dance','debate',
                    'drama', 'gardening', 
                    'music', 
                    'picnics_and_excursion',
                    css_class='col-12 col-md-4 col-lg-4 mb-3'
                ),
                Column(
                    HTML('<h6 class="text-muted">Sports and fitness</h6>'),
                    'skating', 
                    'horse_riding', 
                    'gym',
                    'indoor_sports', 
                    'outdoor_sports', 
                    'swimming_pool', 
                    'karate',
                    'taekwondo', 
                    'yoga',
                    css_class='col-12 col-md-4 col-lg-4 mb-3'
                ),
                
                Column(
                    HTML('<h6 class="text-muted">Disabled friendly</h6>'),
                    'ramps',
                    'washrooms',
                    'elevators',
                    css_class='col-12 col-md-4 col-lg-4 mb-3'
                ),
                css_class='fc_form', id="fc-form"
            ),
            Submit('school-fc-form', 'submit', css_class="col-12 col-md-2 btn btn-sm btn-primary")
        )