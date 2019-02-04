from django import forms

from . import models


class TicketCartForm(forms.Form):
    """ チケットをカートに入れるフォーム

    購入枚数 `amount` という入力を受け取ります。
    入力された値が1以上、チケットの在庫枚数以下の場合にOKとします。

    以下のように引数に `ticket` を渡してください

    >>> ticket = Ticket.objects.get(id=1)
    >>> form = TicketCartForm(ticket=ticket)

    バリデーションチェックする場合にも `ticket` は必要です

    >>> form = TicketCartForm(ticket=ticket, data=request.POST)
    >>> form.is_valid()
    >>> ...

    """
    amount = forms.IntegerField(label="購入枚数", min_value=1, required=True)

    def __init__(self, **kwargs):
        self.ticket = kwargs.pop('ticket')
        super().__init__(**kwargs)

    def clean_amount(self):
        data = self.cleaned_data['amount']

        if data > self.ticket.stock_amount():
            raise forms.ValidationError("在庫が不足しています")

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


