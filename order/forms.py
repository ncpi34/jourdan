from django import forms


class CheckoutForm(forms.Form):
    use_shipping_for_billing = forms.BooleanField(required=False)
    delivery_to = forms.BooleanField(required=False)
    billing_to = forms.BooleanField(required=False)
    delivery_to_id = forms.CharField(required=False,
                                     widget=forms.HiddenInput(
                                         attrs={})
                                     )
    billing_to_id = forms.CharField(required=False,
                                    widget=forms.HiddenInput(
                                        attrs={})
                                    )

    unique_order = forms.CharField(required=False,
                                   widget=forms.HiddenInput(
                                       attrs={
                                           'id': 'unique_order',
                                       })
                                   )

