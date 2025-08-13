from django.shortcuts import render, get_object_or_404, redirect
from .models import UrlEntry
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.utils.timezone import now
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
import json
#import sys
#from django.http import request

# Create your views here.
def indexPage(request): 
    
    tag = request.GET.get('tag', '').strip()
    category = request.GET.get('category', '').strip()
    sub_category = request.GET.get('sub_category', '').strip()
    search_query = request.GET.get('search', '').strip()

    # Base queryset
    url_list = UrlEntry.objects.filter(is_deleted=False)

    # Filter by category
    if category:
        url_list = url_list.filter(
            Q(category__icontains=category) | 
            Q(custom_category__icontains=category)
        )
    # Filter by tag
    if tag:
        url_list = url_list.filter(tags__icontains=tag)
    # Filter by sub-category
    if sub_category:
        url_list = url_list.filter(sub_category__icontains=sub_category)

    # Apply search query
    if search_query:
        url_list = url_list.filter(
            Q(name__icontains=search_query) |
            Q(url__icontains=search_query) |
            Q(tags__icontains=search_query) |
            Q(category__icontains=search_query) |
            Q(custom_category__icontains=search_query) |
            Q(sub_category__icontains=search_query)
        )

    url_list = url_list.order_by('-created_at')
    
    # Debugging prints
    #print("Result count:", url_list.count())
    #print("SQL Query:", url_list.query)
    #sys.stdout.flush()
    
    paginator = Paginator(url_list, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "index.html", {
        "page_obj": page_obj,
        "search_query": search_query,
        "tag": tag,
        "category": category,
        "sub_category": sub_category,
    })
def visit_url(request, pk):
    url_entry = get_object_or_404(UrlEntry, pk=pk, is_deleted=False)
    url_entry.visit_count += 1
    url_entry.save(update_fields=['visit_count'])
    return redirect(url_entry.url)
    
@require_POST
def add_url(request):
    name = request.POST.get("name")
    url = request.POST.get("url")
    category = request.POST.get("category")
    custom_category = request.POST.get("custom_category")
    sub_category = request.POST.get("sub_category")
    tags = request.POST.get("tags")

    if url:
        UrlEntry.objects.create(
            name=name,
            url=url,
            category=category,
            custom_category=custom_category,
            sub_category=sub_category,
            tags=tags
        )
        messages.success(request, "URL saved successfully.")
    else:
        messages.error(request, "URL is required.")

    return redirect("index")
@require_POST
def delete_url(request, pk):
    url_entry = get_object_or_404(UrlEntry, pk=pk, is_deleted=False)
    url_entry.is_deleted = True
    url_entry.deleted_at = now()
    url_entry.save(update_fields=["is_deleted", "deleted_at"])
    messages.success(request, "URL deleted successfully.")
    return redirect('index')

def show_trash(request):
    trashed_urls = UrlEntry.objects.filter(is_deleted=True).order_by('-deleted_at')
    return render(request, 'trash.html', {'trashed_urls': trashed_urls})

def trash_data(request):
    trashed = UrlEntry.objects.filter(is_deleted=True).order_by('-deleted_at')
    paginator = Paginator(trashed, 5)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    rows_html = render_to_string("partials/trash_rows.html", {"page_obj": page_obj})
    pagination_html = render_to_string("partials/trash_pagination.html", {"page_obj": page_obj})

    return JsonResponse({
        "rows_html": rows_html,
        "pagination_html": pagination_html
    })
    
@csrf_exempt
def trash_delete(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        ids = data.get('ids', [])
        UrlEntry.objects.filter(id__in=ids, is_deleted=True).delete()
        return JsonResponse({'status': 'success'})

@csrf_exempt
def trash_recover(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        ids = data.get('ids', [])
        UrlEntry.objects.filter(id__in=ids).update(is_deleted=False, deleted_at=None)
        return JsonResponse({'status': 'success'})
    
def edit_url(request, pk):
    url_entry = get_object_or_404(UrlEntry, pk=pk)

    if request.method == 'POST':
        url_entry.name = request.POST.get('name')
        url_entry.url = request.POST.get('url')
        url_entry.category = request.POST.get('category')
        url_entry.sub_category = request.POST.get('sub_category')
        url_entry.tags = request.POST.get('tags')
        url_entry.save()
        messages.success(request, "URL updated successfully.")
        return redirect('stored-urls')  # or stored_urls_view if separate

    return render(request, 'edit_url.html', {'url': url_entry})

def get_url_details(request, url_id):
    url = UrlEntry.objects.get(pk=url_id)
    return JsonResponse({
        "id": url.id,
        "url": url.url,
        "name": url.name,
        "category": url.category,
        "custom_category": url.custom_category,
        "sub_category": url.sub_category,
        "tags": url.tags,
    })
    
@require_POST
def edit_url_view(request, url_id):
    url = get_object_or_404(UrlEntry, pk=url_id)
    url.url = request.POST.get('url', '')
    url.name = request.POST.get('name', '')
    url.category = request.POST.get('category', '')
    url.custom_category = request.POST.get('custom_category', '')
    url.sub_category = request.POST.get('sub_category', '')
    url.tags = request.POST.get('tags', '')
    url.save()
    return redirect('stored-urls')  # Update to match your view name

@require_POST
def delete_selected(request):
    ids = request.POST.getlist('selected_urls')
    if ids:
        # Move to trash instead of hard delete
        UrlEntry.objects.filter(id__in=ids).update(is_deleted=True)
    return redirect('index')