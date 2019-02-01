from django.core import validators
from django.db import models
from django.urls import reverse

from .validators import StepValueValidator


class Category(models.Model):
    """ カテゴリー

    チケットのカテゴリー。
    管理画面から運営者が設定する。
    """
    name = models.CharField("カテゴリー名", max_length=32)
    extra_fee_rate = models.FloatField('カテゴリーごとの追加手数料',
                                       help_text="カテゴリーごとに持つ追加の販売手数料。"
                                                 "0から1の小数で設定します。",
                                       default=0)
    display_priority = models.IntegerField("表示優先度",
                                           help_text="数字が大きいカテゴリーほど一覧表示で上位に表示されます。")

    class Meta:
        db_table = 'category'
        verbose_name = 'カテゴリー'
        verbose_name_plural = 'カテゴリー'
        ordering = ('-display_priority', 'name')

    def __str__(self):
        return self.name


class Ticket(models.Model):
    """ 販売されているチケット
    """
    STATUS_DISPLAY = 0
    STATUS_STOPPED = 1
    STATUS_SOLD_OUT = 2

    STATUS_CHOICES = (
        (STATUS_DISPLAY, '出品中'),  # 現在出品されている。購入可能な状態
        (STATUS_STOPPED, '出品停止'),  # 以降購入ができない状態。購入済みのチケットは有効
        (STATUS_SOLD_OUT, '完売')  # 出品したチケットが売切れた状態
    )

    seller = models.ForeignKey('tbpauth.User',
                               on_delete=models.CASCADE,
                               related_name='selling_tickets')
    name = models.CharField("チケット名", max_length=128)
    category = models.ForeignKey(Category,
                                 verbose_name="カテゴリー",
                                 on_delete=models.SET_NULL,
                                 null=True, blank=True,
                                 related_name='tickets')
    start_date = models.DateField("開催日")
    price = models.PositiveIntegerField("金額(円)",
                                        validators=[validators.MinValueValidator(100),
                                                    StepValueValidator(100)])
    quantity = models.PositiveIntegerField("販売枚数(枚)",
                                           validators=[validators.MinValueValidator(1)])

    status = models.PositiveIntegerField("販売ステータス", choices=STATUS_CHOICES, default=STATUS_DISPLAY)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ticket'
        verbose_name = 'チケット'
        verbose_name_plural = 'チケット'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tickets:detail', kwargs={'ticket_id': self.id})

    def status_is_display(self):
        """ ステータスが「出品中」の場合にTrueを返す
        """
        return self.status == self.STATUS_DISPLAY

    def fee_rate(self):
        """ 手数料の割合を小数で返す

        販売枚数とカテゴリーの追加手数料から計算して小数で返す
        """
        if self.quantity < 50:
            fee_rate = 0.05
        elif self.quantity < 100:
            fee_rate = 0.03
        else:
            fee_rate = 0.01

        if self.category:
            fee_rate += self.category.extra_fee_rate

        return fee_rate

    def fee(self):
        """ 手数料の金額を返す
        """
        return int(round(self.fee_rate() * self.price))

    def stock_amount(self):
        """ チケットの残り在庫数を返す
        販売枚数から購入履歴 Purchase モデルの合計枚数をマイナスして計算する。
        """
        agg = self.purchases.aggregate(sum_amount=models.Sum('amount'))
        return self.quantity - (agg['sum_amount'] or 0)

    # 以下、表示用の関数。値に単位などを追加して文字列として返す

    def price_display(self):
        return '{:,d}円'.format(self.price)

    def quantity_display(self):
        return '{:,d}枚'.format(self.quantity)

    def fee_rate_display(self):
        return '{:0.0f}％'.format(self.fee_rate() * 100)

    def fee_display(self):
        return '{:,d}円 / 枚'.format(self.fee())

    def stock_amount_display(self):
        return '{:,d}枚'.format(self.stock_amount())
