from . import models
from tbpauth.testing import factory_user


def factory_category(**kwargs):
    """ �e�X�g�p��Category�̃f�[�^�����
    """
    d = {
        'name': '�e�X�g�J�e�S���[',
        'extra_fee_rate': 0.0,
        'display_priority': 0,
    }
    d.update(kwargs)
    return models.Category.objects.create(**d)


def factory_ticket(**kwargs):
    """ �e�X�g�p��Ticket�̃f�[�^�����
    """
    d = {
        'name': '�e�X�g�`�P�b�g',
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
