from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from website.models import Article
import logging
from typing import Union, List

db_logger = logging.getLogger('db')


class ArticleDetailView(DetailView):
    """
    Article Detail
    """
    template_name = 'website/product/product.html'
    queryset = Article.objects.all()
    login_url = ''

    def get_object(self, **kwargs):
        db_logger.info("DEBUT website/product_detail")
        # get arg in url
        _id = self.kwargs.get('pk')
        db_logger.info("recuperation arg dans url")
        try:
            db_logger.info("recuperation arg dans url")
            # find article
            article: Article = Article.objects.get(pk=_id)
            article.nb_views += 1
            article.save()
            db_logger.info(" + 1 et sauvegarde")
            db_logger.info("recuperation arg dans url")
        except Exception as e:
            db_logger.exception(f"erreur (website/product_detail get_object)=> {e}")
        return get_object_or_404(Article, pk=_id)

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        try:
            # update ctx
            db_logger.info("context maj")
        except Exception as e:
            db_logger.exception(f"erreur (website/product_detail get_context_data)=> {e}")
        db_logger.info("FIN website/product_detail")
        return context
