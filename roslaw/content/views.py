from django.views.generic import TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Chapter, Section, Subsection, QA


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "content/dashboard.html"
    login_url = "accounts:login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context.update(
            {
                "published_count": QA.objects.filter(
                    created_by=user, status=QA.STATUS_PUBLISHED
                ).count(),
                "in_review_count": QA.objects.filter(
                    created_by=user, status=QA.STATUS_IN_REVIEW
                ).count(),
                "rejected_count": QA.objects.filter(
                    created_by=user, status=QA.STATUS_REJECTED
                ).count(),
                "chapters": Chapter.objects.all().order_by("order"),
            }
        )

        return context


class ChapterCreateView(LoginRequiredMixin, CreateView):
    model = Chapter
    fields = ["title", "description", "order"]
    success_url = reverse_lazy("content:dashboard")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, "Глава успешно создана.")
        return super().form_valid(form)


class SectionCreateView(LoginRequiredMixin, CreateView):
    model = Section
    fields = ["title", "description", "order"]
    success_url = reverse_lazy("content:dashboard")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        # Add the chapter relationship
        chapter_id = self.request.POST.get("chapter_id")
        if chapter_id:
            self.object.chapters.add(chapter_id)
        messages.success(self.request, "Раздел успешно создан.")
        return response


class SubsectionCreateView(LoginRequiredMixin, CreateView):
    model = Subsection
    fields = ["title", "description", "order"]
    success_url = reverse_lazy("content:dashboard")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)

        section_id = self.request.POST.get("section_id")
        if section_id:
            self.object.sections.add(section_id)
        messages.success(self.request, "Подраздел успешно создан.")
        return response
