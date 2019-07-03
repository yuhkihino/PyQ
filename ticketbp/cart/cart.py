from django.db.transaction import atomic

from purchase.models import Purchase
from tickets.models import Ticket


class Cart:
    def __init__(self, items=None):
        self.items = items or []  # �J�[�g���̏��i (�`�P�b�g�Ȃ�)
        self.edited = False  # �C���X�^���X����ɕҏW�����������̃t���O�B�Z�b�V�����ɕۑ����邩�ǂ����̔���Ɏg��

    def as_json(self):
        ret = []
        for item in self.items:
            ret.append({
                'ticket_id': item['ticket'].id,
                'amount': item['amount'],
            })
        return ret

    @classmethod
    def from_json(cls, items):
        conv_items = []
        for item in items:
            conv_items.append({
                'ticket': Ticket.objects.filter(id=item['ticket_id']).first(),
                'amount': item['amount'],
                'amount_display': '{}��'.format(item['amount'])
            })
        return cls(conv_items)

    def add_ticket(self, ticket, amount):
        """ �J�[�g�Ƀ`�P�b�g��ǉ�����
        """
        self.edited = True
        self.items.insert(0, {
            'ticket': ticket,
            'amount': amount,
            'amount_display': '{}��'.format(amount)
        })

    def delete_ticket(self, ticket):
        """ �J�[�g��������� ticket �����O����
        """
        self.edited = True
        filtered_items = []
        for item in self.items:
            if item['ticket'] != ticket:
                filtered_items.append(item)
        self.items = filtered_items

    def delete_all(self):
        self.edited = True
        self.items = []

    def total_price(self):
        """ ���i�S�Ă̍��v���z���v�Z����
        """
        price = 0
        for item in self.items:
            price += item['ticket'].price * item['amount']
        return price

    def total_price_display(self):
        return '{:,d}�~'.format(self.total_price())

    def check_stock(self):
        """ �݌ɂ��\���ɂ��邩�ǂ����𒲂ׂ�B����ꍇ True�A�Ȃ��ꍇ False ��Ԃ�
        """
        # �`�P�b�g: �w���� �̎����ɕϊ�����
        # �J�[�g���ɓ����`�P�b�g������������Ă���ꍇ��z��
        tickets = {}
        for item in self.items:
            ticket = item['ticket']
            amount = item['amount']
            if ticket in tickets:
                tickets[ticket] += amount
            else:
                tickets[ticket] = amount
        for t, a in tickets.items():
            if t.stock_amount() < a:
                return False
        return True

    def num_items(self):
        return len(self.items)

    @atomic
    def purchase(self, user):
        """ �w�����������s����
        """
        purchases = []
        for item in self.items:
            ticket = item['ticket']
            amount = item['amount']
            # ���؂ꂽ�ꍇ��SOLD_OUT�X�e�[�^�X�ɕύX
            if ticket.stock_amount() == amount:
                ticket.status = Ticket.STATUS_SOLD_OUT
                ticket.save()
            purchases.append(Purchase(
                ticket=ticket,
                user=user,
                amount=amount,
            ))
        Purchase.objects.bulk_create(purchases)
        self.delete_all()
