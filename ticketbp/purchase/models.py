from django.core import validators
from django.db import models


class Purchase(models.Model):
    """ チケットの購入履歴
    """
    ticket = models.ForeignKey('tickets.Ticket',
                               on_delete=models.CASCADE,
                               related_name='purchases')
    user = models.ForeignKey('tbpauth.User',
                             on_delete=models.CASCADE,
                             related_name='purchases')
    amount = models.PositiveIntegerField("購入枚数",
                                         validators=[
                                             validators.MinValueValidator(1),
                                         ])
    bought_at = models.DateTimeField('購入日', auto_now_add=True)

    class Meta:
        db_table = 'purchase'
        verbose_name = '購入履歴'
        verbose_name_plural = '購入履歴'

    def __str__(self):
        return "User {self.user_id} - Ticket {self.ticket_id} ({self.amount})".format(self=self)

    def amount_display(self):
        return '{:,d}枚'.format(self.amount)
