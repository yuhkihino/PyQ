from . import models
from tbpauth.testing import factory_user


def factory_category(**kwargs):
    """ テスト用のCategoryのデータを作る
    """
    d = {
        'name': 'テストカテゴリー',
        'extra_fee_rate': 0.0,
        'display_priority': 0,
    }
    d.update(kwargs)
    return models.Category.objects.create(**d)


def factory_ticket(**kwargs):
    """ テスト用のTicketのデータを作る
    """
    d = {
        'name': 'テストチケット',
        'start_date': '2016-11-05',
        'price': 1000,
        'quantity': 10,
    }
    d.update(kwargs)
    if 'seller' not in d:
        d['seller'] = factory_user()
    if 'category' not in d:
        d['category'] = factory_category()
    return models.Ticket.objects.create(**d)
