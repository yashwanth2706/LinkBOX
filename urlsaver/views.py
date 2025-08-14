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
from .forms import UrlForm
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
    
from django.contrib import messages
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from .forms import UrlForm

@require_POST
def add_url(request):
    # Initialize the form with the submitted POST data
    form = UrlForm(request.POST)

    # Validate the form
    if form.is_valid():
        # If the data is valid, save it as a new object
        form.save()
        return JsonResponse({
            'status': 'success',
            'message': 'URL saved successfully.'
        })
    else:
        # If invalid, return a 400 error with the validation errors
        return JsonResponse({
            'status': 'error',
            'errors': form.errors
        }, status=400)  
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
    url_instance = get_object_or_404(UrlEntry, pk=url_id)
    form = UrlForm(request.POST, instance=url_instance)

    if form.is_valid():
        form.save()
        # On success, return a JSON object with a success status
        return JsonResponse({
            'status': 'success', 
            'message': 'URL updated successfully.'
        })
    else:
        # On failure, return the form errors as JSON
        # status=400 indicates a bad request, which is good practice
        return JsonResponse({
            'status': 'error', 
            'errors': form.errors
        }, status=400)

@require_POST
def delete_selected(request):
    ids = request.POST.getlist('selected_urls')
    if ids:
        # Move to trash instead of hard delete
        UrlEntry.objects.filter(id__in=ids).update(is_deleted=True)
    return redirect('index')

def activity_data(request):
    """
    Provides a JSON response with URL counts for the activity panel.
    """
    total_url_count = UrlEntry.objects.filter(is_deleted=False).count()
    trashed_url_count = UrlEntry.objects.filter(is_deleted=True).count()

    data = {
        'total_url_count': total_url_count,
        'trashed_url_count': trashed_url_count,
    }
    return JsonResponse(data)