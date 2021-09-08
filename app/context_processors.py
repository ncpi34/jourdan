from cart.cart import Cart
from website.models import HomeText, HarborCeilings, CGV, DeliveryText, CartText, GroceryText


def cart(request):
    return {'cart': Cart(request)}


def cart_length(request):
    return {'cartLength': Cart(request).__len__()}


def getCurrentURI(request):
    return {
        'uri': request.path_info
    }


def homeTxt(request):
    home_txt = HomeText.objects.all()
    if home_txt.exists() and home_txt.count() > 0:
        return {'open_hours_txt': home_txt[0]}
    return {'open_hours_txt': ""}


def cgvFile(request):
    cgv_file = CGV.objects.all()
    if cgv_file.exists() and cgv_file.count() > 0:
        return {'cgv_file': cgv_file[0]}
    return {'cgv_file': None}


def harborCeilings(request):
    harbor_ceilings = HarborCeilings.objects.all()
    if harbor_ceilings.exists():
        return {'harbor_ceilings': harbor_ceilings[0]}
    return {'harbor_ceilings': ""}


def get_current_domain(request):
    return {'current_domain': request.get_host()}
