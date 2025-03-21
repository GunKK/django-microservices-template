import os


class PathFormatterMixin:
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if "path" in representation and representation["path"]:
            representation["path"] = (
                f"{os.environ.get('BE_DOMAIN')}{representation['path']}"
            )
        return representation
