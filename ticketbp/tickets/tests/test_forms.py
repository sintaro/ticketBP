from django.test import TestCase

from tickets import forms
from tickets import testing


class TestTicketCartForm(TestCase):
    def test_clean_amount(self):
        ticket = testing.factory_ticket(quantity=800)
        target = forms.TicketCartForm(ticket=ticket,
                                      data={'amount': 800})
        self.assertTrue(target.is_valid())

    def test_clean_amount_too_big(self):
        ticket = testing.factory_ticket(quantity=800)
        target = forms.TicketCartForm(ticket=ticket,
                                      data={'amount': 801})
        self.assertFalse(target.is_valid())
        self.assertEqual(target.errors['amount'], ['在庫が不足しています'])

    def test_clean_amount_too_small(self):
        ticket = testing.factory_ticket(quantity=800)
        target = forms.TicketCartForm(ticket=ticket,
                                      data={'amount': 0})
        self.assertFalse(target.is_valid())
        self.assertEqual(target.errors['amount'], ['この値は 1 以上でなければなりません。'])
