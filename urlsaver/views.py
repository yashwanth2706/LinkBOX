from django.shortcuts import render, get_object_or_404, redirect
from .models import UrlEntry
from django.core.paginator import Paginator
from django.db.models import Q
#from django.http import request

# Create your views here.
def indexPage(request):
    tag = request.GET.get('tag')
    category = request.GET.get('category')
    sub_category = request.GET.get('sub_category')

    urls = UrlEntry.objects.filter(is_deleted=False)

    if tag:
        urls = urls.filter(tags__icontains=tag)
    if category:
        urls = urls.filter(category__iexact=category)
    if sub_category:
        urls = urls.filter(sub_category__iexact=sub_category)

    paginator = Paginator(urls.order_by('-created_at'), 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'index.html', {'page_obj': page_obj})

def visit_url(request, pk):
    url_entry = get_object_or_404(UrlEntry, pk=pk, is_deleted=False)
    url_entry.visit_count += 1
    url_entry.save(update_fields=['visit_count'])
    return redirect(url_entry.url)

def stored_urls_view(request):
    url_list = UrlEntry.objects.filter(is_deleted=False).order_by('-created_at')
    paginator = Paginator(url_list, 10)  # Show 10 URLs per page

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "stored_urls.html", {"page_obj": page_obj})
