from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib import messages
from django.utils.timezone import now
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from .forms import UrlForm
from .forms import SignUpForm, LoginForm
from .models import UrlEntry
import json
from django.core.paginator import Paginator

# -------- Auth views --------
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'auth/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = LoginForm()
    return render(request, 'auth/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

# -------- App views (protected + per-user) --------
@login_required
def index(request):
    tag = request.GET.get('tag', '').strip()
    category = request.GET.get('category', '').strip()
    sub_category = request.GET.get('sub_category', '').strip()
    search_query = request.GET.get('search', '').strip()
    
    show_n_records = request.GET.get('show_n_records', '5').strip()

    # Only current user's, not deleted
    url_list = UrlEntry.objects.filter(user=request.user, is_deleted=False)

    if category:
        url_list = url_list.filter(Q(category__icontains=category) | Q(custom_category__icontains=category))
    if tag:
        url_list = url_list.filter(tags__icontains=tag)
    if sub_category:
        url_list = url_list.filter(sub_category__icontains=sub_category)
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
    
    try:
        per_page = int(show_n_records)
    except ValueError:
        per_page = 5
    
    paginator = Paginator(url_list, int(show_n_records))
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "index.html", {
        "page_obj": page_obj,
        "search_query": search_query,
        "tag": tag,
        "category": category,
        "sub_category": sub_category,
        "show_n_records": per_page,
    })

@login_required
def visit_url(request, pk):
    url_entry = get_object_or_404(UrlEntry, pk=pk, user=request.user, is_deleted=False)
    url_entry.visit_count += 1
    url_entry.save(update_fields=['visit_count'])
    return redirect(url_entry.url)

@require_POST
@login_required
def add_url(request):
    form = UrlForm(request.POST)
    if form.is_valid():
        new_url = form.save(commit=False)
        new_url.user = request.user
        new_url.save()
        return JsonResponse({'status': 'success', 'message': 'URL saved successfully.'})
    return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

@require_POST
@login_required
def delete_url(request, pk):
    url_entry = get_object_or_404(UrlEntry, pk=pk, user=request.user, is_deleted=False)
    url_entry.is_deleted = True
    url_entry.deleted_at = now()
    url_entry.save(update_fields=["is_deleted", "deleted_at"])
    messages.success(request, "URL deleted successfully.")
    return redirect('index')

@login_required
def show_trash(request):
    trashed_urls = UrlEntry.objects.filter(user=request.user, is_deleted=True).order_by('-deleted_at')
    return render(request, 'trash.html', {'trashed_urls': trashed_urls})

@login_required
def trash_data(request):
    trashed = UrlEntry.objects.filter(user=request.user, is_deleted=True).order_by('-deleted_at')
    from django.core.paginator import Paginator
    paginator = Paginator(trashed, 5)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    rows_html = render_to_string("partials/trash_rows.html", {"page_obj": page_obj}, request=request)
    pagination_html = render_to_string("partials/trash_pagination.html", {"page_obj": page_obj}, request=request)
    return JsonResponse({"rows_html": rows_html, "pagination_html": pagination_html})

@csrf_exempt
@login_required
def trash_delete(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        ids = data.get('ids', [])
        # hard delete only user's own trashed items
        UrlEntry.objects.filter(id__in=ids, user=request.user, is_deleted=True).delete()
        return JsonResponse({'status': 'success'})

@csrf_exempt
@login_required
def trash_recover(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        ids = data.get('ids', [])
        UrlEntry.objects.filter(id__in=ids, user=request.user).update(is_deleted=False, deleted_at=None)
        return JsonResponse({'status': 'success'})

@login_required
def get_url_details(request, url_id):
    url = get_object_or_404(UrlEntry, pk=url_id, user=request.user)
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
@login_required
def edit_url_view(request, url_id):
    url_instance = get_object_or_404(UrlEntry, pk=url_id, user=request.user)
    form = UrlForm(request.POST, instance=url_instance)
    if form.is_valid():
        form.save()
        return JsonResponse({'status': 'success', 'message': 'URL updated successfully.'})
    return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

@require_POST
@login_required
def delete_selected(request):
    ids = request.POST.getlist('selected_urls')
    if ids:
        UrlEntry.objects.filter(id__in=ids, user=request.user).update(is_deleted=True, deleted_at=now())
    return redirect('index')

@login_required
def activity_data(request):
    total_url_count = UrlEntry.objects.filter(user=request.user, is_deleted=False).count()
    trashed_url_count = UrlEntry.objects.filter(user=request.user, is_deleted=True).count()
    return JsonResponse({'total_url_count': total_url_count, 'trashed_url_count': trashed_url_count})

