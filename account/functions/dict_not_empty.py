def check_dict_is_not_empty(dictionary):
    """ check dict """
    for item in dictionary:
        if len(dictionary[item]) == 0:
            return False
    else:
        return True
