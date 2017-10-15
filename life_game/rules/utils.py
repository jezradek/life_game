#!/usr/bin/env python


def get_occurence_dict_by_attr(object_l, attr_name):
    """Creates occurrence by attribute dictionary.

    Attributes:
        object_l (Object): Objects to be checked for specific attribute.
        attr_name (str): Attribute name.

    Returns:
        object_attr_d (dict): Occurrence dict indicating occurrence of certain attribute
            among objects.
    """
    object_attr_d = {}

    for object in object_l:
        if object:
            attr = getattr(object, attr_name)
            if attr in object_attr_d.keys():
                object_attr_d[attr] += 1
            else:
                object_attr_d[attr] = 1

    return object_attr_d
