# api/admin.py
from django.contrib import admin
import nested_admin

from api.models import FinalModel, QuestionModel, SlideModel


class SlideModelInline(nested_admin.NestedStackedInline):
    model = SlideModel
    extra = 0
    fields = ("svs_file",)


class QuestionModelInline(nested_admin.NestedStackedInline):
    model = QuestionModel
    extra = 0
    fields = ("clinical_information", "question")
    inlines = [SlideModelInline]   # ← nested slides under each question


@admin.register(FinalModel)
class FinalModelAdmin(nested_admin.NestedModelAdmin):
    list_display = ("creation_date", "model_type", "organ_system", "uploaded_by")
    list_filter = ("creation_date", "model_type", "organ_system", "uploaded_by")
    search_fields = ("model_type", "organ_system__name", "uploaded_by__username")
    inlines = [QuestionModelInline]
