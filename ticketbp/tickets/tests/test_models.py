from django.test import TestCase

from tickets import models
from tickets import testing
from purchase.testing import factory_purchase


class TestTicket(TestCase):
    def test_status_is_display(self):
        target = testing.factory_ticket(status=models.Ticket.STATUS_DISPLAY)
        self.assertTrue(target.status_is_display())

    def test_fee_rate_small_event(self):
        target = testing.factory_ticket(quantity=49)
        self.assertEqual(target.fee_rate(), 0.05)

    def test_fee_rate_middle_event(self):
        target = testing.factory_ticket(quantity=50)
        self.assertEqual(target.fee_rate(), 0.03)

    def test_fee_rate_large_event(self):
        target = testing.factory_ticket(quantity=100)
        self.assertEqual(target.fee_rate(), 0.01)

    def test_fee_rate_with_extra_fee(self):
        category = testing.factory_category(extra_fee_rate=0.05)
        target = testing.factory_ticket(quantity=10, category=category)
        self.assertEqual(target.fee_rate(), 0.1)

    def test_fee(self):
        target = testing.factory_ticket(quantity=10, price=100)
        self.assertEqual(target.fee(), 5)

    def test_stock_amount(self):
        target = testing.factory_ticket(quantity=10)
        factory_purchase(amount=4, ticket=target)
        factory_purchase(amount=5, ticket=target)
        self.assertEqual(target.stock_amount(), 1)

    def test_stock_amount_without_purchase(self):
        target = testing.factory_ticket(quantity=10)
        self.assertEqual(target.stock_amount(), 10)

    def test_price_display(self):
        target = testing.factory_ticket(price=1000)
        self.assertEqual(target.price_display(), '1,000円')

    def test_quantity_display(self):
        target = testing.factory_ticket(quantity=1000)
        self.assertEqual(target.quantity_display(), '1,000枚')

    def test_fee_rate_display(self):
        target = testing.factory_ticket(quantity=100)
        self.assertEqual(target.fee_rate_display(), '1％')

    def test_fee_display(self):
        target = testing.factory_ticket(quantity=100, price=1000)
        self.assertEqual(target.fee_display(), '10円 / 枚')

    def test_stock_amount_display(self):
        target = testing.factory_ticket(quantity=10)
        self.assertEqual(target.stock_amount_display(), '10枚')
