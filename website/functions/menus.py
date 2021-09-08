from django.db.models import Q, Count
from website.models import Group, Family

""" Dynamic menus and submenus from DB"""

list_fam = [
    {"id": 10,
     "name": "Frais", 'url': '#',
     "submenu": {'id': 12,
                 'name': "Test",
                 'url': '#',
                 'subsubmenu': {
                     'id': 2,
                     'name': "Subsub",
                     'url': '#'
                 }

                 }
     }
]


def exclude_groups():
    """
    if less than 10 articles
    """
    articles_by_group = Group.objects.all().annotate(nbre=Count('article_by_group'))
    result = []
    for key, value in enumerate(articles_by_group):
        if value.nbre < 10:
            result.append(articles_by_group[key].name)
    return result


# to get parent menu
def get_menus(request):
    group_query = Group.objects.values_list('name', 'pk')
    groups = [list(i) for i in group_query]
    # groups = list(itertools.chain(*group_query))
    # print(groups)

    liste = [{"id": item[0][1],
              "name": item[0][0], 'url': '#',  # retrieve query to array of dictionnaries
              # 'validators': ["menu_generator.validators.is_authenticated"],
              "submenu": get_families(item[0][0]),
              } for item in zip(groups)]
    # [print(i, '\n') for i in liste]
    return {'menu': liste}


def exclude_families():
    """
    if less than 1 article
    """
    articles_by_family = Family.objects.all().annotate(nbre=Count('article_by_family'))
    result = []
    for key, value in enumerate(articles_by_family):
        if value.nbre < 1:
            result.append(articles_by_family[key].nom)
    return result


# to get families
def get_families(group_name):
    families_query = Family.objects.filter(group__name=group_name).values_list('name', 'pk')
    families = [list(i) for i in families_query]
    liste = []
    for item in range(len(families)):
        temp = {'id': families[item][1],
                'name': families[item][0],
                'url': '#'}
        liste.append(temp)
    # [print(i, '\n') for i in liste]
    return liste


