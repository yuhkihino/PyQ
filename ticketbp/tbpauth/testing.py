import random

from . import models


def factory_user(**kwargs):
    d = {
        'username': ''.join(random.choice('abcdef') for _ in range(10)),
        'first_name': '��',
        'last_name': '��',
        'email': 'test@example.com',
        'address1': '�Z��1',
        'address2': '�Z��2',

    }
    password = kwargs.pop('password', None)
    d.update(kwargs)
    user = models.User(**d)
    if password:
        user.set_password(password)
    user.save()
    return user
