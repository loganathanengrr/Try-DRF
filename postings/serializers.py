from rest_framework import serializers

from .models import BlogPost

class BlogPostSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = BlogPost
        fields = (
            'url',
            'id',
            'user',
            'content',
            'title',
            'timestamp',
        )
        read_only_fields = (
            'id',
            'user',
            'timestamp'
            )
        
    def get_url(self, instance):
        request = self.context.get('request')
        return instance.get_api_url(request=request)

    def validate_title(self, value):
        qs = BlogPost.objects.filter(title__iexact=value)
        if self.instance:
            qs = qs.exclude(id=self.instance.id)
        if qs.exists():
            raise serializers.ValidationError('title already exists')
        return value
    