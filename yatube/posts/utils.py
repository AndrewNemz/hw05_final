from django.core.paginator import Paginator


PAGE_POSTS = 10


def paginator(request, object):
    paginator = Paginator(object, PAGE_POSTS)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return page
