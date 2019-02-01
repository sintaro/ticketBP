from django.db.transaction import atomic

from purchase.models import Purchase
from tickets.models import Ticket


class Cart:
    def __init__(self, items=None):
        self.items = items or []  # カート内の商品 (チケットなど)
        self.edited = False  # インスタンス化後に編集があったかのフラグ。セッションに保存するかどうかの判定に使う

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
                'amount_display': '{}枚'.format(item['amount'])
            })
        return cls(conv_items)

    def add_ticket(self, ticket, amount):
        """ カートにチケットを追加する
        """
        self.edited = True
        self.items.insert(0, {
            'ticket': ticket,
            'amount': amount,
            'amount_display': '{}枚'.format(amount)
        })

    def delete_ticket(self, ticket):
        """ カート内から引数 ticket を除外する
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
        """ 商品全ての合計金額を計算する
        """
        price = 0
        for item in self.items:
            price += item['ticket'].price * item['amount']
        return price

    def total_price_display(self):
        return '{:,d}円'.format(self.total_price())

    def check_stock(self):
        """ 在庫が十分にあるかどうかを調べる。ある場合 True、ない場合 False を返す
        """
        # チケット: 購入数 の辞書に変換する
        # カート内に同じチケットが複数入れられている場合を想定
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
        """ 購入処理を実行する
        """
        purchases = []
        for item in self.items:
            ticket = item['ticket']
            amount = item['amount']
            # 売切れた場合はSOLD_OUTステータスに変更
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
