from django.core.paginator import Paginator


# items_list: expect to be a querySet object
# items_count: the amount of items in one page
# default_page: the dault page that pagination shows
def paginate(request, items_list, items_count=5, default_page=1):
    p = Paginator(items_list, items_count)
    page_number = request.GET.get("page", default_page)
    return p.get_page(page_number)
