# from django.urls import path
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
# from api.views import RegisterCompleteView, RegisterStartView, ChangePasswordView

# urlpatterns = [
#     path("auth/register/", RegisterStartView.as_view(), name="auth-register-start"),
#     path("auth/activate/", RegisterCompleteView.as_view(), name="auth-register-complete"),
#     path("auth/login/", TokenObtainPairView.as_view(), name="auth-login"),
#     path("auth/refresh/", TokenRefreshView.as_view(), name="auth-refresh"),
#     # Auth-only endpoint (global IsAuthenticated applies here):
#     path("auth/change-password/", ChangePasswordView.as_view(), name="auth-change-password"),
# ]

# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api.views import (
    FinalModelViewSet,
    QuestionModelViewSet,
    SlideModelViewSet,
    OrganSystemViewSet,
    StaffUploaderViewSet,
)

router = DefaultRouter()
router.register(r"modules", FinalModelViewSet, basename="finals")
router.register(r"questions", QuestionModelViewSet, basename="questions")
router.register(r"slides", SlideModelViewSet, basename="slides")
router.register(r"organ-systems", OrganSystemViewSet, basename="organ-systems")
router.register(r"staff-uploaders", StaffUploaderViewSet, basename="staff-uploaders")

urlpatterns = [
    # 🔐 JWT auth (matches apiClient.js)
    path("auth/login/",   TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/refresh/", TokenRefreshView.as_view(),    name="token_refresh"),

    # 📦 REST endpoints for your modules/questions/slides/lookups
    path("", include(router.urls)),
]
