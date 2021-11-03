import json
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.views.generic import View

from django.http.response import HttpResponse, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.urls.base import reverse_lazy
from django.core import serializers

from collections import OrderedDict
from typing import List

from django_tables2 import Column, SingleTableMixin, Table
from django_tables2 import SingleTableView

from school_dashboard.models import Application
from schools.models import *
from student_parents.models import Child
from .tables import ApplicationTable
from schools.forms import school_addForm, school_fc_Form




class TableViewMixin(SingleTableMixin):
    # disable pagination to retrieve all data
    table_pagination = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # build list of columns and convert it to an
        # ordered dict to retain ordering of columns
        # the dict maps from column name to its header (verbose name)
        table: Table = self.get_table()
        table_columns: List[Column] = [
            column
            for column in table.columns
        ]

        # retain ordering of columns
        columns_tuples = [(column.name, column.header) for column in table_columns]
        columns: OrderedDict[str, str] = OrderedDict(columns_tuples)

        context['columns'] = columns

        return context

    def get(self, request, *args, **kwargs):
        # trigger filtering to update the resulting queryset
        # needed in case of additional filtering being done
        response = super().get(self, request, *args, **kwargs)
        
        if 'json' in request.GET:
            table: Table = self.get_table()

            data = [
                {column.name: cell for column, cell in row.items()}
                for row in table.paginated_rows
            ]

            return JsonResponse(data, safe=False)
        else:
            return response

class SomeView(TableViewMixin, ListView):
    template_name = 'school_dashboard/student_applications.html'
    table_class = ApplicationTable
    queryset = Application.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['applications'] = 'active'
        return context


"""
School Dashboard Tab
"""
class SchoolDashboard(LoginRequiredMixin, TemplateView):
    template_name = 'school_dashboard/index1.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dashboard'] = 'active'
        return context


"""
Student Appliaction TemplateView
"""
class StudentApplicationsAjax(LoginRequiredMixin, SingleTableView):
    template_name = 'school_dashboard/student_applications.html'



"""
Student Appliaction JSON Response
"""
class StudentApplicationView(LoginRequiredMixin, SingleTableView):
    model = Application
    table_class = ApplicationTable
    template_name = 'school_dashboard/student_applications.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['applications'] = 'active'
        return context

    # def get_queryset(self):
    #     school = School.objects.get(owner=self.request.user)
    #     application = Application.objects.filter(school=school)
    #     return application

    # def get(self, request, *args, **kwargs):
    #     return super().get_context_data(**kwargs)
    #     queryset = self.get_queryset()
    #     application_list = []
    #     for ele in queryset:
    #         application_list.append({
    #             'app_id': ele.application_id, 
    #             'student_name': f"{ele.child.first_name} {ele.child.last_name}",
    #             'dob' : ele.child.date_of_birth,
    #             'app_date': ele.created_at,
    #             'viewed' : ele.viewed,
    #             'status' : ele.status
    #         })
    #     return JsonResponse(application_list, safe=False, status=200)


"""
School Info Tab
"""
class SchoolInfoView(LoginRequiredMixin, DetailView):
    pass

class SchoolInfoCreate(LoginRequiredMixin, CreateView):
    template_name = 'school_dashboard/school_form.html'
    form_class = school_addForm
    success_url = reverse_lazy('school_info')

    def get_object(self, queryset=None):
        obj, created = School.objects.get_or_create(owner=self.request.user)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['school_info'] = 'active'
        return context
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


"""
School Facilities Tab
"""
class SchoolFacilitiesCreateOrUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'school_dashboard/school_facilities.html'
    form_class = school_fc_Form
    success_url = reverse_lazy('school_facilities')

    def get_object(self, queryset=None):
        self.school = get_object_or_404(School, owner=self.request.user)
        obj, created = SchoolFacilities.objects.get_or_create(school=self.school)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['school_facilities'] = 'active'
        return context
    
    def form_valid(self, form):
        form.instance.school = self.school
        return super().form_valid(form)


"""
School Fees GET, POST Ajax
"""
class SchoolFeesView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            school_instance = School.objects.get(owner=request.user)
            school_fee_instance = SchoolFee.objects.filter(school=school_instance)
            serialized_data = serializers.serialize('json', school_fee_instance)
            return JsonResponse({'data': serialized_data}, status=200)
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'School Not Found'}, status=404)
    
        
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


"""
School Fees DELETE AJAX
"""
class SchoolFeeDelete(LoginRequiredMixin, View):
    def post(self, request):
        _id = request.POST.get('id')
        try:
            SchoolFee.objects.get(pk=_id).delete()
            return JsonResponse({'message': 'Deleted successfully'}, status=201)
        except Exception as e:
            return JsonResponse({'message': 'Server error'}, status=400)


"""
School Hall of Fame TemplateView
"""
class SchoolFameView(LoginRequiredMixin, TemplateView):
    template_name = 'school_dashboard/hall_of_fame.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['school_fame'] = 'active'
        return context


"""
School Hall of Fame GET, POST AJAX
"""
class HallofFameAdd(LoginRequiredMixin, View):
    def get(self, request):
        
        school_instance = School.objects.get(owner=request.user)
        instance = HallofFame.objects.filter(school=school_instance)
        sr_data = serializers.serialize('json', instance)
        return JsonResponse({'data': sr_data}, status=200)
    
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


"""
School Hall of Fame DELETE AJAX
"""
class HallofFameDelete(LoginRequiredMixin, View):
    def post(self, request):
        _id = request.POST.get('id')
        try:
            HallofFame.objects.get(pk=_id).delete()
            return JsonResponse({'message': 'Deleted successfully'}, status=201)
        except Exception as e:
            return JsonResponse({'message': 'Server error'}, status=400)


"""
School School Gallery GET, POST and DELETE view
"""
class SchoolGalleryView(LoginRequiredMixin, View):
    def get(self, request):
        try:
            school_instance = School.objects.get(owner=request.user)
            school_gallery = SchoolGallery.objects.filter(school=school_instance)
            ct = {
                'school_gallery': school_gallery,
                'school': school_instance,
                'school_gallery': 'active'
            }
            return render(request, 'school_dashboard/school_gallery.html', context=ct)
        except Exception as e:
            print(e)
            return HttpResponse(f"Error form SchoolGalleryView: {e}")

    def post(self, request):
        try:
            school_instance = School.objects.get(owner=request.user)
            img = request.FILES.get('school-img')

            if img is None:
                return HttpResponse('img not provied')
            instance = SchoolGallery(school=school_instance, school_img=img)
            instance.save()
            return redirect('school_gallery')
        except Exception as e:
            print(e)
            return HttpResponse('You are not authorized!')


@login_required()
def delete_img(request, pk):
    instance = SchoolGallery.objects.get(pk=pk)
    instance.delete()
    return redirect('school_gallery')


"""
School logo POST and DELETE view
"""
@login_required()
def set_school_logo(request):
    if request.method == "POST":
        try:
            school_instance = School.objects.get(owner=request.user)
            img = request.FILES.get('school-img')
            if img is None:
                return HttpResponse('img not provied')
            school_instance.school_logo = img
            school_instance.save()
            return redirect('school_gallery')
        except Exception as e:
            print(e)
            return HttpResponse(e)
    return HttpResponse('Method not allowed!')

@login_required()
def delete_school_logo(request, pk):
    instance = School.objects.get(pk=pk)
    instance.school_logo.delete(save=True)
    return redirect('school_gallery')
