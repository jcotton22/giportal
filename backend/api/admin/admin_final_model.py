from django.contrib import admin
import nested_admin

from api.models import FinalModel, QuestionModel, SlideModel


class SlideModelInline(nested_admin.NestedStackedInline):
    model = SlideModel
    extra = 0
    read_only_fields= ("stem", "thumbnai_path", "dzi_xml_path", "dzi_tiles_path",)
    fields = ("accession_no", "slide_no", "description",)


class QuestionModelInline(nested_admin.NestedStackedInline):
    model = QuestionModel
    extra = 0
    fields = ("clinical_information", "question")
    inlines = [SlideModelInline]   # ← nested slides under each question

@admin.register(SlideModel)
class SlideModelAdmin(admin.ModelAdmin):
    list_display = ("accession_no", "slide_no", "question")
    list_filter = ("accession_no",)
    search_fields = ("accession_no",)
    readonly_fields = ("stem", "thumbnail_path", "dzi_xml_path", "dzi_tiles_path",)



@admin.register(FinalModel)
class FinalModelAdmin(nested_admin.NestedModelAdmin):
    list_display = ("creation_date", "model_type", "organ_system", "uploaded_by")
    list_filter = ("creation_date", "model_type", "organ_system", "uploaded_by")
    search_fields = ("model_type", "organ_system__name", "uploaded_by__username")
    inlines = [QuestionModelInline]
