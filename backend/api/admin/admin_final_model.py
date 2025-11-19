from django.contrib import admin
import nested_admin

from api.models import FinalModel, QuestionModel, SlideModel


class SlideModelInline(nested_admin.NestedStackedInline):
    """
    Inline under QuestionModel so you can add multiple slides per question.
    """
    model = SlideModel
    extra = 0

    # Show derived stuff as read-only
    readonly_fields = ("stem", "thumbnail_path", "dzi_xml_path", "dzi_tiles_path")

    fields = (
        "accession_no",
        "slide_no",
        "description",
        "stem",
        "thumbnail_path",
        "dzi_xml_path",
        "dzi_tiles_path",
    )


class QuestionModelInline(nested_admin.NestedStackedInline):
    """
    Inline under FinalModel so you can add multiple questions per case.
    """
    model = QuestionModel
    extra = 0
    fields = ("clinical_information", "question")
    inlines = [SlideModelInline]   # ← nested slides under each question


@admin.register(SlideModel)
class SlideModelAdmin(admin.ModelAdmin):
    """
    Standalone Slide admin so you can see/imported slides and attach them later
    if needed.
    """
    list_display = ("accession_no", "slide_no", "question")
    list_filter = ("accession_no", "question")
    search_fields = ("accession_no", "slide_no", "description")
    readonly_fields = ("stem", "thumbnail_path", "dzi_xml_path", "dzi_tiles_path")


@admin.register(FinalModel)
class FinalModelAdmin(nested_admin.NestedModelAdmin):
    list_display = ("creation_date", "model_type", "organ_system", "uploaded_by")
    list_filter = ("creation_date", "model_type", "organ_system", "uploaded_by")
    search_fields = ("model_type", "organ_system__name", "uploaded_by__username")
    inlines = [QuestionModelInline]