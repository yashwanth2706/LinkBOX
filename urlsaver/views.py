from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib import messages
from django.utils.timezone import now
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from .forms import UrlForm
from .forms import SignUpForm, LoginForm
from .models import UrlEntry
import json
from django.core.paginator import Paginator
import csv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from django.contrib.auth import views as auth_views
from .forms import CustomAuthenticationForm
import io
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from rest_framework import viewsets
from .serializers import URLSerializer
from .models import UrlEntry
import tldextract # For autonameing urls

def auto_name_from_url(url):
    """
    Extracts a clean name from the given URL.
    Uses tldextract to handle complex TLDs like .co.uk, .org.in, etc.
    Falls back to the full URL if parsing fails.
    """
    try:
        ext = tldextract.extract(url)
        return ext.domain or url
    except Exception:
        return url

class URLViewSet(viewsets.ModelViewSet):
    queryset = UrlEntry.objects.all().order_by('-id')
    serializer_class = URLSerializer

# Landing Page
def landing_page_view(request):
    """
    Renders the public landing page.
    This view is for users who are NOT logged in.
    """
    return render(request, 'linkbox.html')

# -------- Auth views --------
def signup_view(request):
    """
    Renders the signup page.

    If the request is a GET, renders a blank signup form.

    If the request is a POST, validates the form data, and if valid,
    creates a new user, logs them in and redirects them to the index page.
    """
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('urlsaver:index')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def login_view(request):
    """
    Renders the login page.

    If the request is a GET, renders a blank login form.

    If the request is a POST, validates the form data, and if valid,
    logs the user in and redirects them to the index page.
    """
    if request.method == 'POST':
        # Use your custom form here
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('urlsaver:index') # Redirect to index after login
    else:
        # And also here for GET requests
        form = CustomAuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    """
    Logs out the current user and redirects to the login page.

    This view does not accept any arguments other than the standard request
    object.

    Returns an HttpResponseRedirect to the login page.
    """
    logout(request)
    return redirect('urlsaver:login')

# -------- App views (protected + per-user) --------
@login_required
def index(request):
    """
    Renders the main app page for the current user.

    This view requires the user to be logged in.

    The page displays a list of URLs that belong to the current user, with
    filtering and pagination.

    The page also provides a search form that allows the user to search for
    URLs by name, URL, tags, category, custom category, or sub category.

    The page also allows the user to filter the list of URLs by tag, category,
    or sub category.

    The page also allows the user to select how many records to show per page.

    The page also displays a button to add a new URL, a button to delete
    selected URLs, and a button to export all URLs to a CSV file.

    The page also displays a list of URLs that have been deleted by the user.

    :param request: The request object.
    :return: A rendered HTML page.
    """
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
    """
    When the URL's [Visit] button is clicked marks that URL's entry as visited and redirects to the URL.

    Args:
        request: The request object.
        pk: The primary key of the URL entry to visit.

    Returns:
        A redirect response to the URL.
    """

    url_entry = get_object_or_404(UrlEntry, pk=pk, user=request.user, is_deleted=False)
    url_entry.visit_count += 1
    url_entry.save(update_fields=['visit_count'])
    return redirect(url_entry.url)

@require_POST
@login_required
def add_url(request):
    """
    When the [Add URL] button is clicked, this view is called via an AJAX POST request.

    The view validates the form data, and if valid, creates a new URL entry with
    the current user as the owner and saves it to the database. The view then
    returns a JSON response with a status of "success" and a message indicating
    that the URL was saved successfully.

    If the form data is invalid, the view returns a JSON response with a status
    of "error" and a dictionary of errors for each invalid field.

    This view requires the user to be logged in.

    :param request: The request object.
    :return: A JSON response with a status and a message, or a dictionary of errors.
    """
    form = UrlForm(request.POST)
    if form.is_valid():
        new_url = form.save(commit=False)
        new_url.user = request.user
        if not new_url.name.strip():
            new_url.name = auto_name_from_url(new_url.url)
        new_url.save()
        return JsonResponse({'status': 'success', 'message': 'URL saved successfully.'})
    return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

@require_POST
@login_required
def delete_url(request, pk):
    """
    When the checkbox checked for a URL entry and clicked [Delete selected] button, 
    this view is called via an AJAX POST request.

    The view marks the URL entry as deleted by setting is_deleted to True and deleted_at to the current time.
    The view then redirects the user to the home page with a success message indicating that the URL was deleted successfully.

    This view requires the user to be logged in.

    :param request: The request object.
    :param pk: The primary key of the URL entry to delete.
    :return: A redirect response to the home page.
    """
    url_entry = get_object_or_404(UrlEntry, pk=pk, user=request.user, is_deleted=False)
    url_entry.is_deleted = True
    url_entry.deleted_at = now()
    url_entry.save(update_fields=["is_deleted", "deleted_at"])
    messages.success(request, "URL deleted successfully.")
    return redirect('urlsaver:index')

@login_required
def show_trash(request):
    """
    Shows the trash page for the current user.

    The trash page lists all deleted URL entries for the current user, ordered by
    the time they were deleted. The page also provides a button to empty the trash, which deletes
    all deleted URL entries for the current user.

    This view requires the user to be logged in.

    :param request: The request object.
    :return: A rendered HTML page.
    """
    trashed_urls = UrlEntry.objects.filter(user=request.user, is_deleted=True).order_by('-deleted_at')
    return render(request, 'trash.html', {'trashed_urls': trashed_urls})

@login_required
def trash_data(request):
    """
    Returns a JSON response containing the HTML for the trash rows and pagination.

    The HTML for the trash rows is rendered from the "partials/trash_rows.html" template
    and the pagination HTML is rendered from the "partials/trash_pagination.html" template.

    Both templates are rendered with the same context, which includes the page_obj
    containing the list of trashed URL entries, the current page number, and the
    pagination object.

    This view requires the user to be logged in.

    :param request: The request object.
    :return: A JSON response containing the HTML for the trash rows and pagination.
    """
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
    """
    Deletes the specified URL entries from the trash.

    This view requires the user to be logged in.

    This view is called via an AJAX POST request and expects a JSON body with
    a list of IDs of the URL entries to delete.

    The view hard deletes the URL entries from the database.

    :param request: The request object.
    :return: A JSON response with a status of "success" if the URL entries were
        deleted successfully, or a JSON response with a status of "error" if
        there was an error.
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        ids = data.get('ids', [])
        # hard delete only user's own trashed items
        UrlEntry.objects.filter(id__in=ids, user=request.user, is_deleted=True).delete()
        return JsonResponse({'status': 'success'})

@csrf_exempt
@login_required
def trash_recover(request):
    """
    Recovers the specified URL entries from the trash.

    This view requires the user to be logged in.

    This view is called via an AJAX POST request and expects a JSON body with
    a list of IDs of the URL entries to recover.

    The view sets is_deleted to False and deleted_at to None for the specified URL
    entries, effectively "restoring" them from the trash.

    :param request: The request object.
    :return: A JSON response with a status of "success" if the URL entries were
        recovered successfully, or a JSON response with a status of "error" if
        there was an error.
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        ids = data.get('ids', [])
        UrlEntry.objects.filter(id__in=ids, user=request.user).update(is_deleted=False, deleted_at=None)
        return JsonResponse({'status': 'success'})

@login_required
def get_url_details(request, url_id):
    """
    Returns a JSON response containing the details of the specified URL entry.

    This view requires the user to be logged in.

    The view takes a single argument, `url_id`, which is the primary key of the
    URL entry to retrieve.

    The JSON response contains the following keys:

    * `id`: The primary key of the URL entry.
    * `url`: The URL of the URL entry.
    * `name`: The name of the URL entry.
    * `category`: The category of the URL entry.
    * `custom_category`: The custom category of the URL entry.
    * `sub_category`: The sub category of the URL entry.
    * `tags`: The tags of the URL entry.

    :param request: The request object.
    :param url_id: The primary key of the URL entry to retrieve.
    :return: A JSON response containing the details of the URL entry.
    """
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
        url_obj = form.save(commit=False)

        if not url_obj.name.strip():
            url_obj.name = auto_name_from_url(url_obj.url)

        url_obj.save()
        return JsonResponse({'status': 'success', 'message': 'URL updated successfully.'})

    return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

@require_POST
@login_required
def delete_selected(request):
    """
    Deletes the selected URL entries from the index page.

    This view requires the user to be logged in.

    This view is called via an AJAX POST request and expects a list of IDs of the URL entries to delete
    in the request body.

    The view soft deletes the URL entries from the database by setting `is_deleted` to True and
    setting `deleted_at` to the current time.

    :param request: The request object.
    :return: A redirect response to the index page.
    """
    ids = request.POST.getlist('selected_urls')
    if ids:
        UrlEntry.objects.filter(id__in=ids, user=request.user).update(is_deleted=True, deleted_at=now())
    return redirect('urlsaver:index')

@login_required
def activity_data(request):
    """
    Returns the number of total URLs and trashed URLs for the current user as a JSON response.

    The JSON response contains the following keys:

    * `total_url_count`: The number of URLs that are not deleted.
    * `trashed_url_count`: The number of URLs that are deleted.

    This view requires the user to be logged in.

    :param request: The request object.
    :return: A JSON response with the total number of URLs and trashed URLs.
    """
    total_url_count = UrlEntry.objects.filter(user=request.user, is_deleted=False).count()
    trashed_url_count = UrlEntry.objects.filter(user=request.user, is_deleted=True).count()
    return JsonResponse({'total_url_count': total_url_count, 'trashed_url_count': trashed_url_count})

@login_required
def export_selected_csv(request):
    """
    Exports the selected URLs as a CSV file.

    This view requires the user to be logged in.

    This view is called via an AJAX POST request and expects a list of IDs of the URL entries to export
    in the request body.

    The view responds with a text/csv content type and a file attachment with the name "selected_urls.csv",
    containing the exported URLs with their name, URL, category, sub category, and tags.

    :param request: The request object.
    :return: A HTTP response with the exported URLs as a CSV file.
    """
    if request.method == "POST":
        ids = request.POST.getlist("selected_urls[]")  # AJAX sends as array
        urls = UrlEntry.objects.filter(user=request.user, id__in=ids)

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="selected_urls.csv"'

        writer = csv.writer(response)
        writer.writerow(["Name", "URL", "Category", "Sub Category", "Tags"])

        for url in urls:
            writer.writerow([url.name, url.url, url.category, url.sub_category, url.tags])

        return response

    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)

@login_required
def export_selected_pdf(request):
    """
    Exports the selected URLs as a PDF file.

    This view requires the user to be logged in.

    This view is called via an AJAX POST request and expects a list of IDs of the URL entries to export
    in the request body.

    The view responds with a application/pdf content type and a file attachment with the name "urls_export.pdf",
    containing the exported URLs with their name, URL, category, sub category, and tags.

    :param request: The request object.
    :return: A HTTP response with the exported URLs as a PDF file.
    """
    if request.method == "POST":
        selected_ids = request.POST.getlist("selected_urls[]")

        # Exclude deleted URLs
        if selected_ids:
            urls = UrlEntry.objects.filter(id__in=selected_ids, is_deleted=False, user=request.user)
        else:
            confirm_export = request.POST.get("confirm_export")
            if confirm_export != "true":
                return JsonResponse({"error": "no_selection", "message": "No URLs selected. Do you want to export all?"})
            urls = UrlEntry.objects.filter(user=request.user, is_deleted=False)

        if not urls.exists():
            return JsonResponse({"error": "no_data", "message": "No URLs found to export."})

        # Create PDF in memory
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        doc.title = "Selected URLs Export"
        doc.author = request.user.username if request.user.is_authenticated else "LinkBOX"
        doc.subject = "Exported URLs with categories and tags"
        doc.keywords = ["urls", "export", "pdf", "linkbox"]
        elements = []

        styles = getSampleStyleSheet()
        title = Paragraph("LinkBOX URL Export", styles["Heading1"])
        elements.append(title)
        elements.append(Spacer(1, 12))

        # Table Data
        data = [["Name", "URL", "Category", "Sub-Category", "Tags"]]
        for url in urls:
            data.append([
                Paragraph(url.name or "-", styles["Normal"]),
                Paragraph(f'<a href="{url.url}">{url.url}</a>', styles["Normal"]),
                Paragraph(url.category or "-", styles["Normal"]),
                Paragraph(url.sub_category or "-", styles["Normal"]),
                Paragraph(url.tags or "-", styles["Normal"]),
            ])

        # Create Table
        table = Table(data, repeatRows=1)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ]))
        elements.append(table)

        # Build PDF
        doc.build(elements)
        buffer.seek(0)

        # Return Response
        response = HttpResponse(buffer, content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="urls_export.pdf"'
        return response
@login_required
def export_all_pdf(request):
    # Fetch all URLs for the logged-in user that are not deleted
    """
    Exports all URLs for the logged-in user as a PDF file.

    This view requires the user to be logged in.

    The view responds with a application/pdf content type and a file attachment with the name "all_urls_export.pdf",
    containing all URLs with their name, URL, category, sub category, and tags.

    :param request: The request object.
    :return: A HTTP response with the exported URLs as a PDF file.
    """
    urls = UrlEntry.objects.filter(user=request.user, is_deleted=False)

    if not urls.exists():
        return HttpResponse("No URLs found to export.", status=404)

    # Create PDF in memory
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    doc.title = "All URLs Export"
    doc.author = request.user.username
    doc.subject = "Exported URLs with categories and tags"
    doc.keywords = ["urls", "export", "pdf", "linkbox"]
    elements = []

    styles = getSampleStyleSheet()
    title = Paragraph("LinkBOX URL Export - All URLs", styles["Heading1"])
    elements.append(title)
    elements.append(Spacer(1, 12))

    # Table Data
    data = [["Name", "URL", "Category", "Sub-Category", "Tags"]]
    for url in urls:
        data.append([
            Paragraph(url.name or "-", styles["Normal"]),
            Paragraph(f'<a href="{url.url}">{url.url}</a>', styles["Normal"]),
            Paragraph(url.category or "-", styles["Normal"]),
            Paragraph(url.sub_category or "-", styles["Normal"]),
            Paragraph(url.tags or "-", styles["Normal"]),
        ])

    # Create Table
    table = Table(data, repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
    ]))
    elements.append(table)

    # Build PDF
    doc.build(elements)
    buffer.seek(0)

    # Return Response
    response = HttpResponse(buffer, content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="all_urls_export.pdf"'
    return response

@login_required
def export_all_csv(request):
    """
    Exports all URLs for the logged-in user as a CSV file.

    This view requires the user to be logged in.

    The view responds with a text/csv content type and a file attachment with the name "all_urls.csv",
    containing all URLs with their name, URL, category, sub category, and tags.

    :param request: The request object.
    :return: A HTTP response with the exported URLs as a CSV file.
    """
    if request.method == "POST":
        # Get all URLs for the logged-in user that are not deleted
        urls = UrlEntry.objects.filter(user=request.user, is_deleted=False)

        if not urls.exists():
            return HttpResponse("No URLs found to export.", status=404)

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="all_urls.csv"'

        writer = csv.writer(response)
        writer.writerow(["Name", "URL", "Category", "Sub Category", "Tags"])

        for url in urls:
            writer.writerow([url.name, url.url, url.category, url.sub_category, url.tags])

        return response

    return HttpResponse("Invalid request method.", status=400)

@login_required
@require_POST
def import_csv(request):
    """
    Imports a CSV file containing URLs to add to the user's list.

    Expects a CSV file with the following columns:
        - Name
        - URL
        - Category
        - Sub Category
        - Tags

    The URL column is required. If the URL is invalid, it will be skipped.
    If the URL is already active, it will be skipped.
    If the URL is in the trash, it will be restored instead of creating a duplicate.
    New entries will be created for URLs not already present in the user's list.

    If the Name field is blank, a name will be auto-generated from the URL domain.
    Example: https://leetcode.com → "leetcode"
    """
    if not request.FILES.get("csv_file"):
        return JsonResponse({"status": "error", "message": "No file uploaded"}, status=400)

    csv_file = request.FILES["csv_file"]

    # Validate extension
    if not csv_file.name.endswith(".csv"):
        return JsonResponse({"status": "error", "message": "Please upload a valid .csv file"}, status=400)

    # Read CSV
    data_set = csv_file.read().decode("UTF-8")
    io_string = io.StringIO(data_set)
    reader = csv.DictReader(io_string)

    # All CSV headers normalized to lowercase
    reader.fieldnames = [field.lower() for field in reader.fieldnames]

    added, skipped, restored = 0, 0, 0
    url_validator = URLValidator()

    for row in reader:
        raw_url = (row.get("url") or "").strip()
        if not raw_url:
            continue  # skip empty rows

        # Auto-fix scheme if missing
        if not raw_url.startswith(("http://", "https://")):
            raw_url = "https://" + raw_url

        # Validate URL format
        try:
            url_validator(raw_url)
        except ValidationError:
            skipped += 1
            continue

        # If already active → skip
        if UrlEntry.objects.filter(user=request.user, url=raw_url, is_deleted=False).exists():
            skipped += 1
            continue

        # If in trash → restore instead of creating duplicate
        trashed_entry = UrlEntry.objects.filter(user=request.user, url=raw_url, is_deleted=True).first()
        if trashed_entry:
            trashed_entry.is_deleted = False
            trashed_entry.save(update_fields=['is_deleted'])
            restored += 1
            continue

        # Auto-generate name if missing
        name = (row.get("name") or "").strip()
        if not name:
            name = auto_name_from_url(raw_url)

        UrlEntry.objects.create(
            user=request.user,
            name=name,
            url=raw_url,
            category=(row.get("category") or "").strip(),
            sub_category=(row.get("sub category") or "").strip(),
            tags=(row.get("tags") or "").strip(),
        )
        added += 1

    return JsonResponse({
        "status": "success",
        "added": added,
        "restored": restored,
        "skipped": skipped,
        "message": f"Imported {added} new, {restored} restored from trash, {skipped} skipped."
    })
