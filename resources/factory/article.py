from faker import Faker
import random
import json
import codecs


class ArticleData:

    def __init__(self):
        fake = Faker()
        self.name = "produit"
        self.article_code = fake.pystr(min_chars=None, max_chars=10)
        self.conditioning = random.choice([1, 2, 3, 5, 10])
        self.price_without_taxes = fake.pyfloat(left_digits=None,
                                                right_digits=None,
                                                positive=True,
                                                min_value=1.00,
                                                max_value=50.00)
        self.barcode = fake.ean(length=8)
        self.rate_VAT = random.choice([20, 5.5])
        self.stock = random.choice([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
        self.description = fake.sentence(nb_words=10)
        self.picture = ""
        self.price_type = random.choice([1, 2])
        self.capacity = random.choice([1, 1.7, ])
        # self.group = random.choice(
        #     [
        #         {'name': 'frais', 'id': "100-1-49"}, {'name': 'surgelé', 'id': "200-1-49"},
        #         {'name': 'épicerie', 'id': "300-1-49"}, {'name': 'brasserie', 'id': "400-1-49"},
        #         {'name': 'épicerie sucrée', 'id': "500-1-49"}, {'name': 'non alimentaire', 'id': "600-1-49"},
        #         {'name': 'fruits & légumes', 'id': "700-1-49"}
        #     ])
        self.group ={'name': 'frais', 'id': "100-1-49"}
        self.family = random.choice([
            {'name': 'oeufs', 'id': 1}, {'name': 'légumes', 'id': 2}, {'name': 'dessert', 'id': 3},
            {'name': 'patisserie', 'id': 4}, {'name': 'alcool', 'id': 5}, {'name': 'beurre', 'id': 6},
            {'name': 'huile', 'id': 7}, {'name': 'féculents', 'id': 8}, {'name': 'légumes bio', 'id': 9},
            {'name': 'oeufs', 'id': 10}, {'name': 'légumes', 'id': 11}, {'name': 'dessert', 'id': 12},
            {'name': 'patisserie', 'id': 13}, {'name': 'alcool', 'id': 14}, {'name': 'beurre', 'id': 15},
            {'name': 'huile', 'id': 16}, {'name': 'féculents', 'id': 17}, {'name': 'légumes bio', 'id': 18},
            {'name': 'oeufs', 'id': 19}, {'name': 'légumes', 'id': 20}, {'name': 'dessert', 'id': 21},
            {'name': 'patisserie', 'id': 22}, {'name': 'alcool', 'id': 23}, {'name': 'beurre', 'id': 24},
            {'name': 'huile', 'id': 25}, {'name': 'féculents', 'id': 25}, {'name': 'légumes bio', 'id': 26},

        ])
        self.sub_family = random.choice([
            {'name': 'sucre', 'id': 1}, {'name': 'pâtes', 'id': 2}, {'name': 'brocolis', 'id': 3},
            {'name': 'tomates', 'id': 4}, {'name': 'banane', 'id': 5}, {'name': 'pomme', 'id': 6},
            {'name': 'chocolat', 'id': 7}, {'name': 'locaux', 'id': 8}, {'name': 'conserves', 'id': 9}
        ])

    def func_capacity(self, param):
        if param == 1:
            return 1
        return random.choice([1.7, 2.5, 3.2, 1.2])

    def get_json(self, i):
        p = {
            "article_code": self.article_code,
            "price_without_taxes": round(self.price_without_taxes, 2),
            "stock": self.stock,
            "name": f'{self.name}{i}',
            "description": self.description,
            "barcode": self.barcode,
            "rate_VAT": self.rate_VAT,
            "conditioning": self.conditioning,
            # "picture": self.picture,
            "price_type": self.price_type,
            "capacity": self.func_capacity(self.price_type),
            "group": self.group,
            "family": self.family,
            "sub_family": self.sub_family
        }
        return p


def input_data(x):
    data = []
    for i in range(0, x):
        logindata = ArticleData()
        data.append(logindata.get_json(i))

    with open('resources/factory/article.json', "w", encoding="utf-8") as f:
        json.dump(data, f)


def main():
    no_of_input = 1000
    input_data(no_of_input)


main()
