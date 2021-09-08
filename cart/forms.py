from django import forms
from django.core.validators import MaxValueValidator
from django.core.exceptions import ValidationError

from website.models import Article


class CartAddProductForm(forms.Form):
    # def __init__(self, *args, **kwargs):
    #     super().__init__()
    #     super(CartAddProductForm, self).__init__(*args, **kwargs)
    #
    #     qs = dict(*args).get('object_list')
    #
    #     if qs:
    #         for item in qs:
    #             article_quantity = Article.objects.get(libelle=item).quantite
    #             self.fields['quantity'].widget.attrs['max'] = article_quantity

    quantity = forms.IntegerField(label='',
                                  # required=False,
                                  min_value=0,
                                  widget=forms.NumberInput(
                                      attrs={
                                          'class': 'quantity_val',
                                          'style': 'width:3ch; height:3ch;font-size: 3ch;',
                                          'placeholder': '0'})
                                  )
    # quantity = forms.FloatField()
    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput(
                                    attrs={
                                        'class': 'hidden_value'
                                    }
                                ))
    url = forms.CharField(required=False,
                          widget=forms.HiddenInput(
                              attrs={
                                  'class': 'url_to_redirect_after_cart_add',
                              })
                          )


class CartUpdateProductForm(forms.Form):
    # quantity = forms.FloatField()
    quantity = forms.IntegerField(label='',
                                  # required=False,
                                  min_value=0,
                                  widget=forms.NumberInput(
                                      attrs={
                                          'class': 'quantity_val',
                                          'style': 'width:60%; height:100%;font-size: 100%;',
                                          'placeholder': '0'})
                                  )
    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput(
                                    attrs={
                                        'class': 'hidden_value'
                                    }
                                ))
    url = forms.CharField(required=False,
                          widget=forms.HiddenInput(
                              attrs={
                                  'class': 'url_to_redirect_after_cart_add',
                              })
                          )


# formAdd = CartAddProductForm(auto_id=False)


# ... existing code...
# self.fields['price_min'].widget.attrs['max'] = price['price__max']
# self.fields['price_max'].widget.attrs['min'] = price['price__min']
# self.fields['price_max'].widget.attrs['max'] = price['price__max']


class CartCheckAllProductsForm(forms.Form):
    quantity = forms.CharField(required=False,
                               widget=forms.HiddenInput(
                                   attrs={
                                       'id': 'hidden_values',
                                   })
                               )


class CartAddFavoritesForm(forms.Form):
    favorites = forms.CharField(required=True,
                                widget=forms.HiddenInput(
                                    attrs={
                                        'id': 'favorites_to_cart',
                                    })
                                )
