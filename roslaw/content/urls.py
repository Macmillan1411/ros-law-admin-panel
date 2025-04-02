from django.urls import path
from .views import DashboardView
from . import views

app_name = "content"
urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path("chapter/create/", views.ChapterCreateView.as_view(), name="chapter_create"),
    path("section/create/", views.SectionCreateView.as_view(), name="section_create"),
    path(
        "subsection/create/",
        views.SubsectionCreateView.as_view(),
        name="subsection_create",
    ),
]
