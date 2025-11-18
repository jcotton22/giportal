from rest_framework import serializers
from api.models import SlideModel
import os


class SlideModelSerializer(serializers.ModelSerializer):
    # use model properties, but make them absolute URLs if request is present
    thumbnail_url = serializers.SerializerMethodField()
    dzi_xml_url   = serializers.SerializerMethodField()
    dzi_tiles_url = serializers.SerializerMethodField()
    svs_file_url  = serializers.SerializerMethodField()  # now more of a “descriptor”

    class Meta:
        model = SlideModel
        fields = (
            "id",
            "question",
            "accession_no",
            "slide_no",
            "stem",
            "description",
            # optional: include raw stored paths as well
            "thumbnail_path",
            "dzi_xml_path",
            "dzi_tiles_path",
            # computed URLs
            "thumbnail_url",
            "dzi_xml_url",
            "dzi_tiles_url",
        )
        read_only_fields = (
            "id",
            "thumbnail_path",
            "dzi_xml_path",
            "dzi_tiles_path",
            "thumbnail_url",
            "dzi_xml_url",
            "dzi_tiles_url",
        )