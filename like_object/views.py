from rest_framework import viewsets
from like_object.models import LikeObject
from like_object.serializers import LikeObjectSerializer
from django.http.response import Http404
from like_object.permissions import MustBeLoggedIn
from rest_framework.response import Response
from rest_framework import status


class LikeObjectViewSet(viewsets.mixins.CreateModelMixin,
                        viewsets.mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    queryset = LikeObject.objects.all()
    serializer_class = LikeObjectSerializer
    permission_classes = [MustBeLoggedIn]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.profile)

    def get_object(self):
        """
        Override the default get_object() to return a LikeObject
        where the currently logged in user is the author and tweet is
        the selected pk

        In this case get_object() is only called when deleting a like
        """
        try:
            return LikeObject.objects.get(
                author=self.request.user.profile,
                tweet__uuid=self.kwargs['pk'])
        except LikeObject.DoesNotExist:
            raise Http404

    def create(self, request, *args, **kwargs):
        """
        Override the default create method to return a custom
        response message
        """
        response = super().create(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            response.data = {"created": True}
        return response
