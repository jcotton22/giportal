from rest_framework import serializers
from api.models import SlideModel


class SlideModelSerializer(serializers.ModelSerializer):
    # Computed URLs based on the model @property URLs,
    # upgraded to absolute URLs if request is available.
    thumbnail_url = serializers.SerializerMethodField()
    dzi_xml_url = serializers.SerializerMethodField()
    dzi_tiles_url = serializers.SerializerMethodField()

    class Meta:
        model = SlideModel
        fields = (
            "id",
            "question",
            "accession_no",
            "slide_no",
            "stem",
            "description",
            # stored relative paths
            "thumbnail_path",
            "dzi_xml_path",
            "dzi_tiles_path",
            # computed URLs
            "thumbnail_url",
            "dzi_xml_url",
            "dzi_tiles_url",
        )
        # all of these are effectively read-only in the API
        read_only_fields = fields

    def get_thumbnail_url(self, obj):
        """
        Use the model's thumbnail_url property (which already checks storage),
        but make it absolute if we have a request in context.
        """
        request = self.context.get("request")
        url = obj.thumbnail_url  # model @property
        if request and url:
            return request.build_absolute_uri(url)
        return url

    def get_dzi_xml_url(self, obj):
        request = self.context.get("request")
        url = obj.dzi_xml_url
        if request and url:
            return request.build_absolute_uri(url)
        return url

    def get_dzi_tiles_url(self, obj):
        request = self.context.get("request")
        url = obj.dzi_tiles_url
        if request and url:
            return request.build_absolute_uri(url)
        return url