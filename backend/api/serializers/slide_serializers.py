from rest_framework import serializers

from api.models import SlideModel


class SlideModelSerializer(serializers.ModelSerializer):
    # use model properties, but make them absolute URLs if request is present
    thumbnail_url = serializers.SerializerMethodField()
    dzi_xml_url   = serializers.SerializerMethodField()
    dzi_tiles_url = serializers.SerializerMethodField()
    svs_file_url  = serializers.SerializerMethodField()

    class Meta:
        model = SlideModel
        fields = (
            "id",
            "question",
            "svs_file",
            # optional: include raw stored paths as well
            "thumbnail_path",
            "dzi_xml_path",
            "dzi_tiles_path",
            # computed URLs
            "thumbnail_url",
            "dzi_xml_url",
            "dzi_tiles_url",
            "svs_file_url",
        )
        read_only_fields = (
            "id",
            "thumbnail_path",
            "dzi_xml_path",
            "dzi_tiles_path",
            "thumbnail_url",
            "dzi_xml_url",
            "dzi_tiles_url",
            "svs_file_url",
        )

    # ------- helpers -------

    def _abs_url(self, url: str) -> str:
        """
        Take a URL from the model (e.g. '/media/...') and return an
        absolute URL if a request is in context.
        """
        if not url:
            return ""
        request = self.context.get("request")
        return request.build_absolute_uri(url) if request else url

    # ------- getters -------

    def get_thumbnail_url(self, obj) -> str:
        # uses @property thumbnail_url on the model
        return self._abs_url(obj.thumbnail_url)

    def get_dzi_xml_url(self, obj) -> str:
        return self._abs_url(obj.dzi_xml_url)

    def get_dzi_tiles_url(self, obj) -> str:
        return self._abs_url(obj.dzi_tiles_url)

    def get_svs_file_url(self, obj) -> str:
        if not obj.svs_file:
            return ""
        return self._abs_url(obj.svs_file.url)
