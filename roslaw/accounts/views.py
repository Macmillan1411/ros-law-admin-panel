from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, ListView, TemplateView, UpdateView

from .forms import CustomAuthenticationForm, CustomUserCreationForm
from .models import User


class RegisterView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("accounts:waiting_approval")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = True
        user.approved = False
        user.save()
        return redirect(self.success_url)


class WaitingApprovalView(TemplateView):
    template_name = "accounts/waiting_approval.html"


class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = "accounts/login.html"
    redirect_authenticated_user = True


def logout_view(request):
    logout(request)
    messages.success(request, "Вы успешно вышли из системы.")
    return redirect("accounts:login")


class PendingApprovalsView(UserPassesTestMixin, ListView):
    model = User
    template_name = "accounts/pending_approvals.html"
    context_object_name = "pending_users"

    def test_func(self):
        return (
            self.request.user.is_authenticated
            and self.request.user.role == User.SUPERADMIN
        )

    def get_queryset(self):
        return User.objects.filter(approved=False)


class ApproveUserView(UserPassesTestMixin, UpdateView):
    model = User
    fields = []  # No fields needed
    template_name = "accounts/approve_user.html"
    success_url = reverse_lazy("accounts:pending_approvals")

    def test_func(self):
        return (
            self.request.user.is_authenticated
            and self.request.user.role == User.SUPERADMIN
        )

    def get(self, request, *args, **kwargs):
        # for GET request - just display the confirmation page
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # for POST request - approve the user
        self.object = self.get_object()
        self.object.approved = True
        self.object.is_active = True
        self.object.approval_date = timezone.now()
        self.object.save()

        messages.success(
            request, f"Пользователь {self.object.get_full_name()} успешно подтвержден."
        )

        return redirect(self.success_url)
