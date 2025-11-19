from django import forms
from django.contrib import admin
import nested_admin

from api.models import FinalModel, QuestionModel, SlideModel


# ---------------------------------------------------------------------
# 1. Custom form to add a dropdown for existing slides
# ---------------------------------------------------------------------
class QuestionWithSlidesForm(forms.ModelForm):
    existing_slides = forms.ModelMultipleChoiceField(
        queryset=SlideModel.objects.filter(question__isnull=True),
        required=False,
        label="Attach existing slides",
        widget=forms.SelectMultiple(attrs={"style": "width:400px; height:150px"})
    )

    class Meta:
        model = QuestionModel
        fields = ("clinical_information", "question")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Pre-select slides already attached to this question
        if self.instance.pk:
            attached = SlideModel.objects.filter(question=self.instance)
            available = SlideModel.objects.filter(
                models.Q(question__isnull=True) | models.Q(question=self.instance)
            )
            self.fields["existing_slides"].queryset = available
            self.fields["existing_slides"].initial = attached

    def save(self, commit=True):
        instance = super().save(commit=commit)

        if commit:
            selected = self.cleaned_data["existing_slides"]

            # Set selected slides → this question
            SlideModel.objects.filter(pk__in=[s.pk for s in selected]).update(
                question=instance
            )

            # Remove slides that were previously attached but unselected
            SlideModel.objects.filter(question=instance).exclude(
                pk__in=[s.pk for s in selected]
            ).update(question=None)

        return instanceclass QuestionModelInline(nested_admin.NestedStackedInline):
    model = QuestionModel
    form = QuestionWithSlidesForm
    extra = 0

    fields = (
        "clinical_information",
        "question",
        "existing_slides",
    )

    inlines = [SlideModelInline]


# ---------------------------------------------------------------------
# 2. Inline for Slides (read-only view)
# ---------------------------------------------------------------------
class SlideModelInline(nested_admin.NestedStackedInline):
    """
    Inline under QuestionModel so you can view slides per question.
    """
    model = SlideModel
    extra = 0

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


# ---------------------------------------------------------------------
# 3. Inline for Questions (with dropdown for existing slides)
# ---------------------------------------------------------------------
class QuestionModelInline(nested_admin.NestedStackedInline):
    """
    Inline under FinalModel so you can add multiple questions per case.
    Also lets you select existing slides from a dropdown.
    """
    model = QuestionModel
    form = QuestionWithSlidesForm
    extra = 0
    fields = (
        "clinical_information",
        "question",
        "existing_slides",   # dropdown multi-select
    )
    inlines = [SlideModelInline]   # nested slides visible below each question


# ---------------------------------------------------------------------
# 4. Admin for SlideModel (standalone)
# ---------------------------------------------------------------------
@admin.register(SlideModel)
class SlideModelAdmin(admin.ModelAdmin):
    """
    Standalone Slide admin so you can see/import slides and attach them later
    if needed.
    """
    list_display = ("accession_no", "slide_no", "question")
    list_filter = ("accession_no", "question")
    search_fields = ("accession_no", "slide_no", "description")
    readonly_fields = ("stem", "thumbnail_path", "dzi_xml_path", "dzi_tiles_path")


# ---------------------------------------------------------------------
# 5. Admin for FinalModel (top level)
# ---------------------------------------------------------------------
@admin.register(FinalModel)
class FinalModelAdmin(nested_admin.NestedModelAdmin):
    list_display = ("creation_date", "model_type", "organ_system", "uploaded_by")
    list_filter = ("creation_date", "model_type", "organ_system", "uploaded_by")
    search_fields = ("model_type", "organ_system__name", "uploaded_by__username")
    inlines = [QuestionModelInline]