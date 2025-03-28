from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Chapter, Section, Subsection, QA

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'content/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Get user stats
        context.update({
            'published_count': QA.objects.filter(created_by=user, status=QA.STATUS_PUBLISHED).count(),
            'in_review_count': QA.objects.filter(created_by=user, status=QA.STATUS_IN_REVIEW).count(),
            'rejected_count': QA.objects.filter(created_by=user, status=QA.STATUS_REJECTED).count(),
        })
        
        # Get all chapters
        context['chapters'] = Chapter.objects.all().order_by('order')
        
        # Get active items from query parameters
        active_chapter_id = self.request.GET.get('chapter', None)
        active_section_id = self.request.GET.get('section', None)
        active_subsection_id = self.request.GET.get('subsection', None)
        
        # If no chapter is specified, use the first one as default
        if not active_chapter_id and context['chapters'].exists():
            active_chapter_id = context['chapters'].first().id
        
        # If a chapter is specified, get its sections
        if active_chapter_id:
            active_chapter_id = int(active_chapter_id)
            context['active_chapter'] = active_chapter_id
            context['active_sections'] = Section.objects.filter(
                chapters__id=active_chapter_id
            ).order_by('order')
            
            # If no section is specified and there are sections, use the first one
            if not active_section_id and context['active_sections'].exists():
                active_section_id = context['active_sections'].first().id
        
        # If a section is specified, get its subsections
        if active_section_id:
            active_section_id = int(active_section_id)
            context['active_section'] = active_section_id
            context['active_subsections'] = Subsection.objects.filter(
                sections__id=active_section_id
            ).order_by('order')
            
            # If no subsection is specified and there are subsections, use the first one
            if not active_subsection_id and context['active_subsections'].exists():
                active_subsection_id = context['active_subsections'].first().id
        
        # If a subsection is specified, get its QA items
        if active_subsection_id:
            active_subsection_id = int(active_subsection_id)
            context['active_subsection'] = active_subsection_id
            
            # QA items displayed depend on user role
            if user.is_content_admin() or user.is_moderator():
                # Admins and moderators see all QA items
                context['active_qa_items'] = QA.objects.filter(
                    subsections__id=active_subsection_id
                ).order_by('title')
            else:
                # Editors see only published items and their own items
                context['active_qa_items'] = QA.objects.filter(
                    subsections__id=active_subsection_id
                ).filter(
                    status=QA.STATUS_PUBLISHED
                ).order_by('title')
                
                # Add user's own items that aren't published
                user_items = QA.objects.filter(
                    subsections__id=active_subsection_id,
                    created_by=user
                ).exclude(status=QA.STATUS_PUBLISHED)
                
                if user_items.exists():
                    context['active_qa_items'] = list(context['active_qa_items']) + list(user_items)
        
        return context


class QAListView(LoginRequiredMixin, TemplateView):
    template_name = 'content/qa_list.html'
    # add more implementation to this one


class QACreateView(LoginRequiredMixin, TemplateView):
    template_name = 'content/qa_create.html'
    # add more to this

