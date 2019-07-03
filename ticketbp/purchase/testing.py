from purchase import models
from tbpauth.testing import factory_user
from tickets.testing import factory_ticket


def factory_purchase(**kwargs):
    """ テスト用のPurchaseのデータを作る
    """
    d = {
        'amount': 10,
    }
    d.update(kwargs)
    if 'ticket' not in d:
        d['ticket'] = factory_ticket()
    if 'user' not in d:
        d['user'] = factory_user()
    return models.Purchase.objects.create(**d)
