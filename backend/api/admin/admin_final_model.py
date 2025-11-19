import os

from django import forms
from django.conf import settings
from django.contrib import admin
import nested_admin

from api.models import FinalModel, QuestionModel, SlideModel


# ============================
# Helper: list available DZI files
# ============================
def get_dzi_choices():
    """
    Scan settings.DZI_ROOT for *.dzi and return (stem, label) choices.

    Example file:
        media/dzi/pls24-005960-a3.dzi
    ->  stem = "pls24-005960-a3"
    """
    root = settings.DZI_ROOT
    if not os.path.isdir(root):
        return []

    choices = []
    for name in os.listdir(root):
        if not name.lower().endswith(".dzi"):
            continue
        stem = os.path.splitext(name)[0]
        label = stem.upper()   # You can change the label later
        choices.append((stem, label))

    return sorted(choices, key=lambda x: x[1])


# ============================
# Slide form (for inline + direct admin)
# ============================
class SlideModelInlineForm(forms.ModelForm):
    # Extra field ONLY for admin UI – not stored directly on the model
    dzi_choice = forms.ChoiceField(
        label="Converted slide (DZI)",
        required=True,
        choices=[],
        help_text="Pick the pre-converted slide from media/dzi.",
    )

    class Meta:
        model = SlideModel
        # Only model fields – dzi_choice is extra
        fields = ("accession_no", "slide_no", "description")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Populate choices from actual DZI files on disk
        self.fields["dzi_choice"].choices = get_dzi_choices()

        # Pre-select current stem if editing an existing slide
        if self.instance and self.instance.pk and self.instance.stem:
            self.fields["dzi_choice"].initial = self.instance.stem

    def save(self, commit=True):
        """
        Use dzi_choice to set the model's `stem`.

        SlideModel.save() will then derive:
          - thumbnail_path
          - dzi_xml_path
          - dzi_tiles_path
        from stem.
        """
        obj = super().save(commit=False)
        stem = self.cleaned_data["dzi_choice"]
        obj.stem = stem

        if commit:
            obj.save()

        return obj


# ============================
# Inline: Slide under Question
# ============================
class SlideModelInline(nested_admin.NestedStackedInline):
    model = SlideModel
    form = SlideModelInlineForm
    extra = 0

    readonly_fields = ("stem", "thumbnail_path", "dzi_xml_path", "dzi_tiles_path")
    fields = (
        "accession_no",
        "slide_no",
        "description",
        "dzi_choice",       # dropdown to select converted slide
        "stem",
        "thumbnail_path",
        "dzi_xml_path",
        "dzi_tiles_path",
    )


# ============================
# Inline: Question under FinalModel
# ============================
class QuestionModelInline(nested_admin.NestedStackedInline):
    model = QuestionModel
    extra = 0
    fields = ("clinical_information", "question")
    inlines = [SlideModelInline]   # nested slides under each question


# ============================
# Admin: Slide (standalone view)
# ============================
@admin.register(SlideModel)
class SlideModelAdmin(admin.ModelAdmin):
    form = SlideModelInlineForm

    list_display = ("accession_no", "slide_no", "question")
    list_filter = ("accession_no",)
    search_fields = ("accession_no", "slide_no")

    readonly_fields = ("stem", "thumbnail_path", "dzi_xml_path", "dzi_tiles_path")
    fields = (
        "question",
        "accession_no",
        "slide_no",
        "description",
        "dzi_choice",       # same dropdown as inline
        "stem",
        "thumbnail_path",
        "dzi_xml_path",
        "dzi_tiles_path",
    )


# ============================
# Admin: FinalModel
# ============================
@admin.register(FinalModel)
class FinalModelAdmin(nested_admin.NestedModelAdmin):
    list_display = ("creation_date", "model_type", "organ_system", "uploaded_by")
    list_filter = ("creation_date", "model_type", "organ_system", "uploaded_by")
    search_fields = ("model_type", "organ_system__name", "uploaded_by__username")
    inlines = [QuestionModelInline]