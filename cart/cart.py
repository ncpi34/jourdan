from decimal import Decimal
from django.conf import settings
from django.shortcuts import redirect
from website.models import Article

"""Cart Module"""


class Cart(object):

    def __init__(self, request):
        """
        Initialization
        """
        self.request = request
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        """
        Iterate over the items in the cart and get products from DB
        """
        products_ids = self.cart.keys()
        # get the product obj and add them to the cart
        products = Article.objects.filter(id__in=products_ids)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['total_price'] = round(float(item['price_with_taxes']) * float(item['quantity']), 2)
            yield item

    def __len__(self):
        """
        Count all items in the cart
        """
        return len(self.cart.values())

    def add(self, product, quantity=None, update_quantity=False):
        """
        Add a product to the cart or update its quantity.
        """
        if product.price_with_taxes > 0 and quantity != "0":
            self.cart[str(product.id)] = {
                'user_id': self.request.user.id,
                'article_id': str(product.id),
                'name': product.name,
                'quantity': quantity,
                'price_type': product.price_type,
                'price_with_taxes': str(product.price_with_taxes),
                'article_code': product.article_code,
            }
        self.save()

    def save(self):
        # update the session cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # mark the session as "modified" to make sure it is saved
        self.session.modified = True

    def remove(self, product):
        """
        Remove a product from the cart.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def get_total_price(self):
        """
        Get price of the cart
        """
        return round(sum(Decimal(float(item['price_with_taxes']) * float(item['quantity'])) for item in self.cart.values()), 2)

    def clear(self):
        """
        Remove cart from session
        """
        del self.cart
        self.save()

    def clear_all(self, products):
        """
        Remove all item in cart
        """
        for product in products:
                product_id = str(product['article_id'])
                if product_id in self.cart:
                    del self.cart[product_id]
                    self.save()

    def decrement(self, product):
        """
        In case of decrementing
        """
        for key, value in self.cart.items():
            if key == str(product.id):
                value['quantity'] = value['quantity'] - 1
                if value['quantity'] < 1:
                    return redirect('cart:cart_detail')
                self.save()
                break
            else:
                print("Erreur panier")

    def join_total_TTC(self):
        total = str(self.get_total_price()).split('.')
        return "".join(total)
