from django.views.generic import ListView
from cart.forms import CartAddProductForm
from website.models import HomeText, Novelties, Article, Cart, DeliveryText, GroceryText, CartText
import logging

db_logger = logging.getLogger('db')


class HomeView(ListView):
    """
    Home View
    only http get allowed
    """
    template_name = 'website/home.html'
    ordering = ['libelle']
    context_object_name = 'articles'
    login_url = ''

    def get_queryset(self):
        cart_articles: [Cart] = Cart.objects.all()
        # empty qs
        if not cart_articles.exists():
            db_logger.info("website/home/get_queryset : empty")
            return None

        # retrieve data and append
        articles: [Article] = []
        for i in cart_articles:
            articles.append(i.get_article())
        db_logger.info(f"website/home/get_queryset data: {articles}")
        return articles

    def get_context_data(self, **kwargs) -> object:
        """
        Get context Data
        Args:
            **kwargs:

        Returns: object
        """
        db_logger.info("DEBUT website/home")
        context = super(HomeView, self).get_context_data(**kwargs)
        # adding form to products
        context['form'] = CartAddProductForm(auto_id=False)

        # queryset
        qs_delivery: [DeliveryText] = DeliveryText.objects.all().first()
        qs_cart: [CartText] = CartText.objects.all().first()
        qs_grocery: [GroceryText] = GroceryText.objects.all().first()

        try:
            # update context
            context.update({
                'delivery_txt': qs_delivery,
                'grocery_txt': qs_grocery,
                'cart_txt': qs_cart,

            })
            db_logger.info("pas d'erreur maj context")
        except Exception as e:
            db_logger.exception(f"erreur maj context (website/home)=> {e}")
        db_logger.info("FIN website/home")
        return context
