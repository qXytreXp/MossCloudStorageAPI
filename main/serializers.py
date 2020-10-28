from rest_framework import serializers
from .models import Document


class DocumentListSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Document
        fields = ('user', 'document', 'type_file', 'time_created',)

