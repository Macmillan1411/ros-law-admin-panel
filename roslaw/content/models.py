from django.db import models
from django.conf import settings

class Chapter(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order']

class Section(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    chapters = models.ManyToManyField(Chapter, related_name='sections')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order']

class Subsection(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    sections = models.ManyToManyField(Section, related_name='subsections')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order']

class QA(models.Model):
    STATUS_DRAFT = 'draft'
    STATUS_IN_REVIEW = 'in_review'
    STATUS_APPROVED = 'approved'
    STATUS_REJECTED = 'rejected'
    STATUS_PUBLISHED = 'published'

    STATUS_CHOICES = [
        (STATUS_DRAFT, 'Draft'),
        (STATUS_IN_REVIEW, 'In Review'),
        (STATUS_APPROVED, 'Approved'),
        (STATUS_REJECTED, 'Rejected'),
        (STATUS_PUBLISHED, 'Published'),
    ]

    title = models.CharField(max_length=255)
    question_content = models.TextField()
    answer_content = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_DRAFT)
    subsections = models.ManyToManyField(Subsection, related_name='qa_items')

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='created_qas',
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    moderated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='moderated_qas',
        null=True, blank=True
    )
    moderated_at = models.DateTimeField(null=True, blank=True)

    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.title