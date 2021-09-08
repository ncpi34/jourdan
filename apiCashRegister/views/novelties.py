from django.http import Http404
from rest_framework.views import APIView
from apiCashRegister.serializers import NoveltiesSerializer, ArticleSerializer
from website.models import Article, Novelties
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework import status


class NoveltiesList(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser,)

    def get(self, request, format=None):
        sells = Novelties.objects.all()
        serializer = NoveltiesSerializer(sells, many=True)
        return Response(serializer.data)


class NoveltiesDetail(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser,)

    def get_novelties(self, pk):
        try:
            return Novelties.objects.get(pk=pk)
        except Novelties.DoesNotExist:
            raise Http404

    def get_article(self, pk):
        try:
            return Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            raise Http404

    def post(self, request, pk, format=None):
        article = self.get_article(pk)
        serializer = ArticleSerializer(article)
        novelties = Novelties.objects.all().count()
        if novelties < 25:
            novelties = Novelties(article=article)
            novelties.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_507_INSUFFICIENT_STORAGE)

    def delete(self, request, pk, format=None):
        novelties = self.get_novelties(pk)
        novelties.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
