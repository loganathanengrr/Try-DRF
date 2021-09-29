from django.shortcuts import render
from django.db.models import Q
from rest_framework import (
    generics, 
    permissions, 
    mixins
)

from .models import BlogPost
from .serializers import BlogPostSerializer
from .permissions import ISOwnerOrReadOnly

# Create your views here.

class BlogPostAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    lookup_field = 'id'
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('q', None)
        if query is not None:
            lookup = Q(title__iexact=query) | Q(content__iexact=query)
            qs = qs.filter(lookup).distinct()
        
        return qs
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def get_serializer_context(self, *args, **kwargs):
        context = super().get_serializer_context(*args, **kwargs)
        context['request'] = self.request
        return context

class BlogPostRUDView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    serializer_class = BlogPostSerializer
    permission_classes = [ISOwnerOrReadOnly, ]
    queryset = BlogPost.objects.all()

    def get_queryset(self):
        return super().get_queryset()
    
    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
    
    def get_serializer_context(self, *args, **kwargs):
        context = super().get_serializer_context(*args, **kwargs)
        context['request'] = self.request
        return context
