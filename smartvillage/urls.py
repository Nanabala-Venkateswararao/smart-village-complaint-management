from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from complaints import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("complaints/new/", views.create_complaint, name="create_complaint"),
    path("complaints/<int:pk>/", views.complaint_detail, name="complaint_detail"),
    path("official/", views.official_dashboard, name="official_dashboard"),
    path("official/complaints/<int:pk>/update/", views.update_complaint, name="update_complaint"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
