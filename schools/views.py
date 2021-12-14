from django.views.generic.base import View
from django.http.response import JsonResponse
from django.core import serializers
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator
from school_dashboard import models
from schools.filterset import SchoolFilter

from student_parents.models import Child

from .forms import *
from schools.forms import school_addForm
from schools.models import School, SchoolDetail, SchoolFee, SchoolReviews

def index(request):
    return render(request, 'schools/index.html', {})
    

class FilteredListView(ListView):
    filterset_class = None
    
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filterset.qs.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        has_filter = any(field in self.request.GET for field in set(self.filterset.get_fields()))
        context['filterset'] = self.filterset
        context['has_filter'] = has_filter
        return context

class SchoolListView(FilteredListView):
    filterset_class = SchoolFilter
    model = School
    paginate_by = 12 # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['filterset'] = self.filterset
        return context

class SchoolDetailView(View):
    template_name = 'schools/school_detail.html'

    def get(self, request, pk):
        school = get_object_or_404(School, id=pk)
        school_details = get_object_or_404(SchoolDetail, school=school)
        school_facilities = get_object_or_404(SchoolFacilities, school=school)
        school_reviews = SchoolReviews.objects.filter(school=school_details)
        context = {
            'sfc': school_facilities,
            'sd': school_details,
            'school': school,
            'school_reviews': school_reviews
        }
        return render(request, self.template_name, context)

  
    def post(self, request, pk):
        if self.request.user.is_authenticated:
            _rating = request.POST.get('rating')
            _comment = request.POST.get('comment')
            _school_obj = get_object_or_404(School, id=pk)
            _school__details_obj = get_object_or_404(SchoolDetail, school=_school_obj)
            _user = self.request.user

            obj = SchoolReviews(user=_user, comment=_comment, rating=_rating, school=_school__details_obj)
            obj.save()
            return JsonResponse({'message': 'Your review has been successfully recorded'}, status=200)
        return JsonResponse({'message': 'Please Login First'}, status=400)


def compare_schools(request):
    return render(request, 'schools/compare_schools.html', {})


def get_school_reviews(request, pk):
    school = get_object_or_404(School, id=pk)
    sd_obj = get_object_or_404(SchoolDetail, school=school)
    reviews = SchoolReviews.objects.filter(school=sd_obj).order_by('-created_at')
    paginator = Paginator(reviews, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if int(page_number) > paginator.num_pages:
        return JsonResponse({'message': 'No more reviews'}, status=400)
    sr_data = serializers.serialize('json', page_obj, use_natural_foreign_keys=True)
    return JsonResponse(sr_data, safe=False, status=200)


def delete_school_reviews(request, pk, reviewId):
    try:
        review = SchoolReviews.objects.get(pk=reviewId)
        if request.user.id == review.user.id:
            review.delete()
            return JsonResponse({'message': 'Review deleted successfully' }, status=200)
        else:
            return JsonResponse({'message': 'You don\'t have permission'}, status=403)
    except Exception as e:
        print(e)
        return JsonResponse({'message': 'review not fond' }, status=404)