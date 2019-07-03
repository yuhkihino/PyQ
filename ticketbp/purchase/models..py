from django.core import validators
from django.db import models


class Purchase(models.Model):
    """ ƒ`ƒPƒbƒg‚Ìw“ü—š—ğ
    """
    ticket = models.ForeignKey('tickets.Ticket',
                               on_delete=models.CASCADE,
                               related_name='purchases')
    user = models.ForeignKey('tbpauth.User',
                             on_delete=models.CASCADE,
                             related_name='purchases')
    amount = models.PositiveIntegerField("w“ü–‡”",
                                         validators=[
                                             validators.MinValueValidator(1),
                                         ])
    bought_at = models.DateTimeField('w“ü“ú', auto_now_add=True)

    class Meta:
        db_table = 'purchase'
        verbose_name = 'w“ü—š—ğ'
        verbose_name_plural = 'w“ü—š—ğ'

    def __str__(self):
        return "User {self.user_id} - Ticket {self.ticket_id} ({self.amount})".format(self=self)

    def amount_display(self):
        return '{:,d}–‡'.format(self.amount)
