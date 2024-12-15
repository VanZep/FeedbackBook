from rest_framework import mixins, viewsets, filters

from .permissions import IsAdminOrReadOnlyPermission


class ListCreateDestroy(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):

    permission_classes = (IsAdminOrReadOnlyPermission,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^slug', '^name')
    lookup_field = 'slug'
