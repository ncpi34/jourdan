from django.http import Http404
from rest_framework.viewsets import ModelViewSet
from apiCashRegister.functions import IsSuperUser
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework import status
from datetime import datetime
from django.core.files.base import ContentFile

from apiCashRegister.serializers import ArticleSerializer
from website.models import Article, Group, Family
import base64


class ArticleViewSet(ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (IsAuthenticated, IsSuperUser,)
    lookup_field = 'article_code'
    update_data_pk_field = 'article_code'

    def perform_create(self, serializer):
        serializer.save()

    def create(self, request, *args, **kwargs):
        kwarg_field: str = self.lookup_url_kwarg or self.lookup_field
        if isinstance(request.data, dict):
            self.kwargs[kwarg_field] = request.data[self.update_data_pk_field]
            try:
                return self.update(request, *args, **kwargs)
            except Http404:
                return super().create(request, *args, **kwargs)
        elif isinstance(request.data, list):
            data: list = request.data
            serializer: ArticleSerializer = ArticleSerializer(data=data, many=True)
            serializer.is_valid(raise_exception=False)
            for item in request.data:
                d_item_data: dict = self.treatment_nested_fields(item)
                Article.objects.update_or_create(article_code=item.get('article_code', None), defaults={**d_item_data})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        if isinstance(request.data, dict):
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
        else:
            partial = kwargs.pop('partial', False)
            instance = self.filter_queryset(self.get_queryset())
            data = [request.data] * instance.count()
            serializer = self.get_serializer(instance, data, many=True, partial=partial)

        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def treatment_nested_fields(self, validated_data):
        if 'group' in validated_data:
            data_group: dict = dict(validated_data.pop('group'))
            group = self.treatment_group(data_group)
            validated_data.update(group)
            if 'family' in validated_data:
                data_family: dict = dict(validated_data.pop('family'))
                family = self.treatment_family(data_family, group['group'])
                validated_data.update(family)
        if 'picture' in validated_data:
            data_picture = validated_data.pop('picture')
            picture = self.treatment_file(data_picture)
            validated_data.update(picture)
        return validated_data

    @staticmethod
    def treatment_file(data):
        try:
            _format, _img_str = data.split(';base64,')
            _name, ext = _format.split('/')
            # if no content
            if not _img_str:
                return False
            now = datetime.now()
            name = now.strftime("%Y%m%d%H%M%S%f")[:-3]
            return {"picture": ContentFile(base64.b64decode(_img_str), name=f'{name}.{ext}')}
        except Exception:
            pass

    @staticmethod
    def treatment_group(data):
        print(data)
        print(data.get('name'))
        return {"group": Group.objects.update_or_create(id=data.get('id'),
                                                        defaults={'name': data.get('name')})[0],

                }
        # return {"group": Group.objects.get_or_create(name=data.get('name'))[0]}

    @staticmethod
    def treatment_family(data, group):
        return {"family": Family.objects.update_or_create(group=group,
                                                          name=data.get('name'))[0]}
