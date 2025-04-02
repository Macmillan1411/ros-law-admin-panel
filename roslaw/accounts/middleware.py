from django.shortcuts import redirect
from django.urls import reverse


class ApprovalMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Exclude login, register, logout, and waiting pages from the check
        excluded_paths = [
            reverse("accounts:login"),
            reverse("accounts:register"),
            reverse("accounts:logout"),
            reverse("accounts:waiting_approval"),
            "/admin/",  # Also exclude Django admin
        ]

        # Check if the path is in excluded paths
        path_excluded = any(request.path.startswith(path) for path in excluded_paths)

        # If user is authenticated but not approved, redirect to waiting page
        if (
            request.user.is_authenticated
            and not request.user.approved
            and not path_excluded
            and not request.user.role == "superadmin"
        ):  # Superadmins bypass approval
            return redirect("accounts:waiting_approval")

        response = self.get_response(request)
        return response
