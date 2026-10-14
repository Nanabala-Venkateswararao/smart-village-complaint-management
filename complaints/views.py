from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from .forms import RegisterForm, ComplaintForm, OfficialUpdateForm
from .models import Complaint

def home(request):
    stats = {
        "total": Complaint.objects.count(),
        "resolved": Complaint.objects.filter(status=Complaint.Status.RESOLVED).count(),
    }
    return render(request, "home.html", {"stats": stats})

def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        user.email = form.cleaned_data["email"]
        user.first_name = form.cleaned_data["first_name"]
        user.save()
        login(request, user)
        messages.success(request, "Your account has been created.")
        return redirect("dashboard")
    return render(request, "register.html", {"form": form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    error = None
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("official_dashboard" if user.is_staff else "dashboard")
        error = "Invalid username or password."
    return render(request, "login.html", {"error": error})

@login_required
def logout_view(request):
    if request.method == "POST":
        logout(request)
        messages.info(request, "You have logged out.")
        return redirect("home")
    return render(request, "confirm_logout.html")

@login_required
def dashboard(request):
    query = request.GET.get("q", "").strip()
    complaints = Complaint.objects.filter(citizen=request.user)
    if query:
        complaints = complaints.filter(
            Q(title__icontains=query) |
            Q(category__icontains=query) |
            Q(village_location__icontains=query) |
            Q(status__icontains=query)
        )
    return render(request, "dashboard.html", {"complaints": complaints, "query": query})

@login_required
def create_complaint(request):
    form = ComplaintForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        complaint = form.save(commit=False)
        complaint.citizen = request.user
        complaint.save()
        messages.success(request, f"Complaint #{complaint.pk} submitted successfully.")
        return redirect("complaint_detail", pk=complaint.pk)
    return render(request, "create_complaint.html", {"form": form})

@login_required
def complaint_detail(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    if complaint.citizen_id != request.user.id and not request.user.is_staff:
        messages.error(request, "You cannot view that complaint.")
        return redirect("dashboard")
    return render(request, "complaint_detail.html", {"complaint": complaint})

def staff_check(user):
    return user.is_authenticated and user.is_staff

@user_passes_test(staff_check, login_url="login")
def official_dashboard(request):
    query = request.GET.get("q", "").strip()
    status = request.GET.get("status", "").strip()
    complaints = Complaint.objects.select_related("citizen").all()
    if query:
        complaints = complaints.filter(
            Q(title__icontains=query) |
            Q(village_location__icontains=query) |
            Q(citizen__username__icontains=query)
        )
    if status in Complaint.Status.values:
        complaints = complaints.filter(status=status)
    return render(request, "official_dashboard.html", {
        "complaints": complaints, "query": query, "selected_status": status,
        "statuses": Complaint.Status.choices,
    })

@user_passes_test(staff_check, login_url="login")
def update_complaint(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    form = OfficialUpdateForm(request.POST or None, instance=complaint)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, f"Complaint #{complaint.pk} updated.")
        return redirect("official_dashboard")
    return render(request, "update_complaint.html", {"form": form, "complaint": complaint})
