from faker import Faker
import random
import json


class EnterpriseData:

    def __init__(self):
        fake = Faker()
        self.name = "type"

    def get_json(self, i):
        p = {
            "id": i,
            "name": f'{self.name}{i}',
        }
        return p


def input_data(x):
    data = []
    for i in range(0, x):
        logindata = EnterpriseData()
        data.append(logindata.get_json(i))

    with open('resources/factory/enterprise_type.json', "w") as f:
        json.dump(data, f)


def main():
    no_of_input = 20
    input_data(no_of_input)


main()