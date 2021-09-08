from django.views.generic import ListView
from website.filters import ArticleFilter
from website.models import Article
from django.db.models import Q
import logging
from typing import Union, List

db_logger = logging.getLogger('db')


class ArticleView(ListView):
    """
    Products views
    """
    template_name = 'website/product/products.html'
    paginate_by = 60
    context_object_name = 'articles'

    def get_ordering(self):
        db_logger.info("DEBUT website/products get_ordering")
        if self.request.GET.get('ordering'):
            db_logger.info("GET.ordering non present")
            return [self.request.GET.get('ordering')]
        else:
            db_logger.info("GET.ordering present")
            return ['name']

    def order_by(self):
        result: str = self.request.GET.get('ordering') or 'price_with_taxes'
        return result

    def get_queryset(self):
        db_logger.info("DEBUT website/products get_queryset")
        # exclude products with price <= 0.00
        query = Q(price_with_taxes__gt=0)
        article = Article.objects
        order_by_price = self.order_by()
        # filter Article with param in url
        if self.request.GET.get('q'):
            db_logger.info("parametre q trouve")
            q_search = self.request.GET.get('q')
            query.add(Q(article_code__contains=q_search), Q.AND)
            query.add(Q(article_code__contains=q_search.upper()), Q.OR)

            query.add(Q(name__startswith=q_search.upper()), Q.OR)
            query.add(Q(name__startswith=q_search.lower()), Q.OR)
            query.add(Q(name__startswith=q_search.capitalize()), Q.OR)

            query.add(Q(name__contains=q_search.upper()), Q.OR)
            query.add(Q(name__contains=q_search.lower()), Q.OR)
            db_logger.info("avant le renvoi de l'objet filtré")
            return article.filter(query).order_by(*self.get_ordering())

        elif self.kwargs.get('subfamily'):
            db_logger.info("parametre subfamily trouve")
            _subfamily = self.kwargs.get("subfamily")
            query.add(Q(sub_family__pk=_subfamily), Q.AND)
            if self.request.GET.get('price'):
                db_logger.info("parametre price trouve")
                price = int(self.request.GET.get('price'))
                vat = self.request.GET.get('vat')
                query.add(Q(price_with_taxes__range=(0, price)), Q.AND)
                if vat != 'All':
                    db_logger.info("parametre vat != ALL")
                    query.add(Q(rate_VAT=vat), Q.AND)
                db_logger.info("avant le renvoi de l'objet filtré")
                return article.filter(query).order_by(order_by_price)
            db_logger.info("avant le renvoi de l'objet filtré")
            return article.filter(query).order_by(*self.get_ordering())

        elif self.kwargs.get('family'):
            db_logger.info("parametre family trouve")
            _family = self.kwargs.get("family")
            query.add(Q(family__pk=_family), Q.AND)
            if self.request.GET.get('price'):
                db_logger.info("parametre price trouve")
                price = int(self.request.GET.get('price'))
                vat = self.request.GET.get('vat')
                query.add(Q(price_with_taxes__range=(0, price)), Q.AND)
                if vat == 'All':
                    db_logger.info("parametre vat == ALL")
                    db_logger.info("avant le renvoi de l'objet filtré")
                    return article.filter(query).order_by(order_by_price)

                query.add(Q(rate_VAT=vat), Q.AND)
                db_logger.info("avant le renvoi de l'objet filtré")
                return article.filter(query).order_by(order_by_price)
            db_logger.info("avant le renvoi de l'objet filtré")
            return article.filter(query).order_by(*self.get_ordering())

        elif self.kwargs.get('group'):
            _group = self.kwargs.get("group")
            query.add(Q(group__pk=_group), Q.AND)
            if self.request.GET.get('price'):
                db_logger.info("parametre price trouve")
                price = int(self.request.GET.get('price'))
                vat = self.request.GET.get('vat')
                query.add(Q(price_with_taxes__range=(0, price)), Q.AND)
                if vat != 'All':
                    db_logger.info("parametre vat != ALL")
                    query.add(Q(rate_VAT=vat), Q.AND)
                db_logger.info("avant le renvoi de l'objet filtré")
                return article.prefetch_related('group').filter(query).order_by(order_by_price)

            return article.filter(query).order_by(*self.get_ordering())
        elif self.request.GET.get('price'):
            price = int(self.request.GET.get('price'))
            vat = self.request.GET.get('vat')
            query.add(Q(price_with_taxes__range=(0, price)), Q.AND)
            if vat != 'All':
                db_logger.info("parametre vat != ALL")
                query.add(Q(price_with_taxes__range=(0, price)), Q.AND)
            db_logger.info("avant le renvoi de l'objet filtré")
            return article.filter(query).order_by(
                order_by_price)
        else:
            db_logger.info("aucun parametre trouve")
            return article.filter(query).order_by(order_by_price)

    def get_context_data(self, **kwargs):
        db_logger.info("DEBUT website/products get_context_data")
        context = super(ArticleView, self).get_context_data(**kwargs)
        # update ctx
        context['filter'] = ArticleFilter()
        db_logger.info("contexte maj")
        db_logger.info("FIN website/products get_context_data")
        return context
