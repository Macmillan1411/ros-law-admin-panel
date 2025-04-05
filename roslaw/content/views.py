from django.views.generic import TemplateView, CreateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from .models import Chapter, Section, Subsection, QA


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "content/dashboard.html"
    login_url = "accounts:login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Get active items from query parameters
        active_chapter_id = self.request.GET.get("chapter", None)
        active_section_id = self.request.GET.get("section", None)
        active_subsection_id = self.request.GET.get("subsection", None)

        chapters = Chapter.objects.all().order_by("order")

        if not active_chapter_id and chapters.exists():
            active_chapter_id = chapters.first().id

        active_sections = []
        if active_chapter_id:
            active_chapter_id = int(active_chapter_id)
            active_sections = Section.objects.filter(
                chapters__id=active_chapter_id
            ).order_by("order")

            if not active_section_id and active_sections.exists():
                active_section_id = active_sections.first().id

        active_subsections = []
        if active_section_id:
            active_section_id = int(active_section_id)
            active_subsections = Subsection.objects.filter(
                sections__id=active_section_id
            ).order_by("order")

            if not active_subsection_id and active_subsections.exists():
                active_subsection_id = active_subsections.first().id

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
                "chapters": chapters,
                "active_chapter_id": active_chapter_id,
                "active_section_id": active_section_id,
                "active_subsection_id": active_subsection_id,
                "active_sections": active_sections,
                "active_subsections": active_subsections,
            }
        )

        if active_subsection_id:
            active_subsection_id = int(active_subsection_id)
            if user.is_content_admin() or user.is_moderator():
                qa_items = QA.objects.filter(
                    subsections__id=active_subsection_id
                ).order_by("title")
            else:
                qa_items = QA.objects.filter(
                    subsections__id=active_subsection_id, status=QA.STATUS_PUBLISHED
                ).order_by("title")

                user_items = QA.objects.filter(
                    subsections__id=active_subsection_id, created_by=user
                ).exclude(status=QA.STATUS_PUBLISHED)

                if user_items.exists():
                    qa_items = list(qa_items) + list(user_items)

            context["active_qa_items"] = qa_items

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


class QACreateView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        title = request.POST.get("title")
        content = request.POST.get("content")
        subsection_id = request.POST.get("subsection_id")

        # Validate input
        if not title or not content or not subsection_id:
            return JsonResponse({"error": "Missing required fields"}, status=400)

        try:
            subsection = Subsection.objects.get(id=subsection_id)

            qa = QA.objects.create(
                title=title,
                question_content=title,  # Using title as the question content
                answer_content=content,
                status=QA.STATUS_DRAFT,
                created_by=request.user,
            )

            qa.subsections.add(subsection)

            messages.success(request, "Вопрос-ответ успешно создан.")
            return JsonResponse({"success": True, "qa_id": qa.id})

        except Subsection.DoesNotExist:
            return JsonResponse({"error": "Подраздел не найден"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
