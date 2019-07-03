from django import forms

from . import models


class TicketCartForm(forms.Form):
    """ �`�P�b�g���J�[�g�ɓ����t�H�[��

    �w������ `amount` �Ƃ������͂��󂯎��܂��B
    ���͂��ꂽ�l��1�ȏ�A�`�P�b�g�̍݌ɖ����ȉ��̏ꍇ��OK�Ƃ��܂��B

    �ȉ��̂悤�Ɉ����� `ticket` ��n���Ă�������

    >>> ticket = Ticket.objects.get(id=1)
    >>> form = TicketCartForm(ticket=ticket)

    �o���f�[�V�����`�F�b�N����ꍇ�ɂ� `ticket` �͕K�v�ł�

    >>> form = TicketCartForm(ticket=ticket, data=request.POST)
    >>> form.is_valid()
    >>> ...

    """
    amount = forms.IntegerField(label="�w������", min_value=1, required=True)

    def __init__(self, **kwargs):
        self.ticket = kwargs.pop('ticket')
        super().__init__(**kwargs)

    def clean_amount(self):
        data = self.cleaned_data['amount']

        if data > self.ticket.stock_amount():
            raise forms.ValidationError("�݌ɂ��s�����Ă��܂�")

        return data


class TicketSellingForm(forms.ModelForm):
    class Meta:
        model = models.Ticket
        fields = (
            'name',
            'category',
            'start_date',
            'price',
            'quantity',
        )
