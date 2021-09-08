from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import ListView
from django.views.generic.base import View
from website.models import Article, FavoritesClient, Group
from django.shortcuts import redirect, get_object_or_404
import logging

db_logger = logging.getLogger('db')


class FavoritesView(LoginRequiredMixin, ListView):
    """
    Favorites View
    only http get allowed
    """
    template_name = 'website/product/favorites.html'
    ordering = ['name']
    context_object_name = 'articles'
    obj = None

    def get_queryset(self) -> object:
        try:
            db_logger.info("DEBUT website/favorites")

            # request preparation in DB
            query = Q(article_favorite__user=self.request.user)
            db_logger.info("prepartion requete BDD ok")

            # filter with query, order to use in get_context_data
            self.obj: [Article] = Article.objects.filter(query).order_by('group__id')
            db_logger.info(f"resultat requete: {self.obj}")

            db_logger.info("fin methode get_queryset")
            return self.obj
        except Exception as e:
            db_logger.exception(f"erreur (website/favorites FavoritesView.get_queryset)=> {e}")
            return

    def get_context_data(self, **kwargs):
        db_logger.info("dans la methode get_context_data")
        # override
        context = super(FavoritesView, self).get_context_data(**kwargs)
        db_logger.info("apres la surcharge de methode")
        try:
            # update context
            context['groups']: [Group] = Group.objects.filter(
                Q(article_by_group__in=[i.id for i in self.obj])
            ).distinct()
            db_logger.info("attribution du context[groups] ok")
        except Exception as e:
            db_logger.exception(f"erreur (website/favorites FavoritesView.get_context_data)=> {e}")
        db_logger.info("FIN website/favorites")
        return context


class CancelFavoritesView(LoginRequiredMixin, View):
    """
    Cancel Favorites Views
    """
    def post(self, *args, **kwargs):
        """ post method """
        try:
            db_logger.info("DEBUT website/home CancelFavoritesView")
            # find favorite with arg inn url
            favorite: FavoritesClient = get_object_or_404(FavoritesClient, article_id=kwargs['pk'], user=self.request.user)
            db_logger.info("favoris trouvé")
            # delete favorite
            favorite.delete()
            db_logger.info("favoris supprime")
            # flash message
            messages.info(self.request, 'Favori supprimé')
            db_logger.info("message envoyé dans le template")
        except Exception as e:
            db_logger.exception(f"erreur (website/home CancelFavoritesView)=> {e}")
        db_logger.info("FIN website/home CancelFavoritesView")

        return redirect('website:favorites')
