from datetime import datetime
from django.conf import settings
from django.core.files.base import ContentFile
from rest_framework import serializers
from website.models import Article, Group, Family
import base64


class ImageSerializerField(serializers.Field):
    def to_representation(self, value):
        return f"{settings.CURRENT_SITE + 'media/' + str(value)}"

    def to_internal_value(self, data):
        try:
            _format, _img_str = data.split(';base64,')

            _name, ext = _format.split('/')

            # no data
            if _name is None:
                return
            now = datetime.now()
            name = now.strftime("%Y%m%d%H%M%S%f")[:-3]
            return ContentFile(base64.b64decode(_img_str), name=f'{name}.{ext}')
        except Exception:
            pass


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']


class FamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = Family
        fields = ['id', 'name']



class ArticleListSerializer(serializers.ListSerializer):
    def update(self, instance, validated_data):
        # Maps for id->instance and id->data item.
        book_mapping = {book.id: book for book in instance}
        data_mapping = {item['id']: item for item in validated_data}

        # Perform creations and updates.
        ret: [] = []
        for book_id, data in data_mapping.items():
            book = book_mapping.get(book_id, None)
            if book is None:
                ret.append(self.child.create(data))
            else:
                ret.append(self.child.update(book, data))

        # Perform deletions.
        for book_id, book in book_mapping.items():
            if book_id not in data_mapping:
                book.delete()

        return ret


class ArticleSerializer(serializers.ModelSerializer):
    group = GroupSerializer(required=False)
    family = FamilySerializer(required=False)
    picture = ImageSerializerField(required=False)

    class Meta:
        list_serializer_class = ArticleListSerializer
        model = Article
        fields = ['id', 'name', 'price_with_taxes', 'price_type', 'article_code',
                  'group', 'family', 'description', 'picture']

    @staticmethod
    def treatment_group(data):
        print(data)
        return {"group": Group.objects.get_or_create(name=data.get('name'))[0]}

    @staticmethod
    def treatment_family(data, group):
        return {"family": Family.objects.get_or_create(group=group,
                                                       name=data.get('name'))[0]}

    def treatment_nested_fields(self, validated_data):
        if 'group' in validated_data:
            data_group: dict = dict(validated_data.pop('group'))
            group = self.treatment_group(data_group)
            validated_data.update(group)
            if 'family' in validated_data:
                data_family: dict = dict(validated_data.pop('family'))
                family = self.treatment_family(data_family, group['group'])
                validated_data.update(family)
        return validated_data

    def create(self, validated_data):
        validated_data = self.treatment_nested_fields(validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        print('self => ', self)
        print('instance =>', instance)
        print('validated_data=>', validated_data)
        validated_data = self.treatment_nested_fields(validated_data)
        return super().update(instance, validated_data)
        # info = model_meta.get_field_info(instance)
        #
        # # Simply set each attribute on the instance, and then save it.
        # # Note that unlike `.create()` we don't need to treat many-to-many
        # # relationships as being a special case. During updates we already
        # # have an instance pk for the relationships to be associated with.
        # m2m_fields = []
        # for attr, value in validated_data.items():
        #     if attr in info.relations and info.relations[attr].to_many:
        #         m2m_fields.append((attr, value))
        #     else:
        #         setattr(instance, attr, value)
        #
        # instance.save()
        #
        # # Note that many-to-many fields are set after updating instance.
        # # Setting m2m fields triggers signals which could potentially change
        # # updated instance and we do not want it to collide with .update()
        # for attr, value in m2m_fields:
        #     field = getattr(instance, attr)
        #     field.set(value)
        #
        # return instance
