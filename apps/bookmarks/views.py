from rest_framework import viewsets, filters, status, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import BookMark
from .serializers import BookMarkSerializer
from django.db.models import Q


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user


class BookMarkViewSet(viewsets.ModelViewSet):
    """
        User bookmark manager
    """
    serializers_class = BookMarkSerializer
    queryset = BookMark.objects.all()
    serializer_class = BookMarkSerializer

    search_fields = ['title', 'url']
    ordering_fields = ['title']

    def create(self, request):
        """
        Create Method for new bookmarks
        """
        serializer = self.serializers_class(data=request.data)

        if serializer.is_valid():
            serializer.validated_data['user'] = request.user
            serializer.save()

            return Response(
                {'status': 'Saved'}, status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def get_queryset(self):
        """
        User view restriction to see private bookmarks create from another users.
        Anonymous users can only view public bookmarks
        """
        queryset = self.queryset
        query_set = queryset.filter(is_public=True)
        if not self.request.user.is_anonymous:
            query_set = queryset.filter(Q(is_public=True) | Q(user=self.request.user.id))

        return query_set

    def get_permissions(self):
        if self.action in ('update', 'partial_update'):
            self.permission_classes = [IsOwner, ]
        return super(self.__class__, self).get_permissions()
