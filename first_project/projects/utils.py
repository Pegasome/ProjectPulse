from .models import Project,Tag
from django.db.models import Q
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage

def paginateProjects(request, projects, results):
    page = request.GET.get('page', 1)
    results_per_page = results
    paginator = Paginator(projects, results_per_page)
 
    try:
        custom_range = paginator.get_elided_page_range(number=page, on_each_side=1, on_ends=1)
        projects = paginator.page(number=page)
    except PageNotAnInteger:
        page = 1
        custom_range = paginator.get_elided_page_range(number=page, on_each_side=1, on_ends=1)
        projects = paginator.page(number=page)
    except EmptyPage:
        page = paginator.num_pages
        custom_range = paginator.get_elided_page_range(number=page, on_each_side=1, on_ends=1)
        projects = paginator.page(number=page)
 
    return custom_range , projects, paginator

def searchProjects(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    tags = Tag.objects.filter(name__icontains = search_query)

    projects = Project.objects.distinct().filter(
        Q(title__icontains = search_query) |
        Q(description__icontains = search_query) |
        Q(owner__name__icontains = search_query) |
        Q(tags__in = tags)

    )
    return projects, search_query
