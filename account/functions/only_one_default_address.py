from django.db.models import Q

from account.models import Address


def only_one_default_address_by_type(request, address, dictionary=False):
    """ save only one default """
    if not dictionary:
        try:
            old_default = Address.objects.get(
                Q(user=request.user) & Q(default_address=True) & Q(address_type=address.address_type)
            )
            old_default.default_address = False
            old_default.save()
            address.default_address = True
            address.save()
        except Address.DoesNotExist:
            address.default_address = True
            address.save()
    else:
        try:
            old_default = Address.objects.get(
                Q(user=request.user) & Q(default_address=True) & Q(address_type=address['type']))
            old_default.default_address = False
            old_default.save()
        except Address.DoesNotExist:
            pass
