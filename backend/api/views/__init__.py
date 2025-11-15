from .register_start_view import RegisterStartView
from .register_complete_view import RegisterCompleteView
from .change_password_view import ChangePasswordView

# new ones
from .final_model_view import FinalModelViewSet
from .questions_view import QuestionModelViewSet
from .slides_view import SlideModelViewSet
from .lookup_views import OrganSystemViewSet, StaffUploaderViewSet

__all__ = [
    # existing
    "RegisterStartView",
    "RegisterCompleteView",
    "ChangePasswordView",
    # new
    "FinalModelViewSet",
    "QuestionModelViewSet",
    "SlideModelViewSet",
    "OrganSystemViewSet",
    "StaffUploaderViewSet",
]
