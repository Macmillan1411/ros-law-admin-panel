from django.contrib import admin
from .models import Chapter, Section, Subsection, QA

class ChapterAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    search_fields = ('title',)

class SectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    search_fields = ('title',)
    filter_horizontal = ('chapters',)

class SubsectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    search_fields = ('title',)
    filter_horizontal = ('sections',)

class QAAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'created_by', 'created_at', 'is_published')
    list_filter = ('status', 'is_published')
    search_fields = ('title', 'question_content', 'answer_content')
    filter_horizontal = ('subsections',)
    readonly_fields = ('created_by', 'created_at', 'moderated_by', 'moderated_at')

admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Subsection, SubsectionAdmin)
admin.site.register(QA, QAAdmin)