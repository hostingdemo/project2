from django.views.generic.base import View
from django.http.response import JsonResponse
from django.core import serializers
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import render
from django.core.paginator import Paginator

from .forms import *
from schools.forms import school_addForm
from schools.models import School, SchoolDetail, SchoolFee, SchoolReviews

def index(request):
    return render(request, 'schools/index.html', {})

def update_school(request):
    pass


class SchoolListView(ListView):
    model = School
    paginate_by = 12 # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class SchoolDetailView(DetailView):
    model = SchoolDetail
    template_name = 'schools/school_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            _rating = request.POST.get('rating')
            _comment = request.POST.get('comment')
            _school_obj = self.get_object()
            _user = self.request.user

            obj = SchoolReviews(user=_user, comment=_comment, rating=_rating, school=_school_obj)
            obj.save()
            return JsonResponse({'message': 'Your review has been successfully recorded'}, status=200)
        return JsonResponse({'message': 'Please Login First'}, status=400)


def compare_schools(request):
    return render(request, 'schools/compare_schools.html', {})


def get_school_reviews(request, pk):
    school = SchoolDetail.objects.get(pk=pk)
    reviews = SchoolReviews.objects.filter(school= school).order_by('-created_at').all()
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
            return JsonResponse({'message': 'review deleted' }, status=200)
        else:
            return JsonResponse({'message': 'You don\'t have permission'}, status=403)
    except Exception as e:
        print(e)
        return JsonResponse({'message': 'review not fond' }, status=404)