from django.urls import path

from . import views

app_name = "accounts"
urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path(
        "waiting-approval/",
        views.WaitingApprovalView.as_view(),
        name="waiting_approval",
    ),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", views.logout_view, name="logout"),
    path(
        "pending-approvals/",
        views.PendingApprovalsView.as_view(),
        name="pending_approvals",
    ),
    path(
        "approve-user/<int:pk>/", views.ApproveUserView.as_view(), name="approve_user"
    ),
]
