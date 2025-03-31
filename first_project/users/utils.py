from .models import Profile,Skill
from django.db.models import Q 
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage

def paginateProfiles(request, profiles, results):
    page = request.GET.get('page', 1)
    results_per_page = results
    paginator = Paginator(profiles, results_per_page)
 
    try:
        custom_range = paginator.get_elided_page_range(number=page, on_each_side=1, on_ends=1)
        profiles = paginator.page(number=page)
    except PageNotAnInteger:
        page = 1
        custom_range = paginator.get_elided_page_range(number=page, on_each_side=1, on_ends=1)
        profiles = paginator.page(number=page)
    except EmptyPage:
        page = paginator.num_pages
        custom_range = paginator.get_elided_page_range(number=page, on_each_side=1, on_ends=1)
        profiles = paginator.page(number=page)
 
    return custom_range , profiles, paginator


def searchProfiles(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
    
    skills = Skill.objects.filter(name__icontains=search_query)

    profiles = Profile.objects.distinct().filter(Q(name__icontains=search_query) | Q(short_intro__icontains=search_query) | Q(skill__in = skills))

    return profiles, search_query
    
