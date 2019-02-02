from django.test import TestCase
from django.urls import reverse

from tickets import models
from tickets import testing
from tbpauth.testing import factory_user


class TestTicketList(TestCase):
    def _getTarget(self):
        return reverse('tickets:list')

    def test_get(self):
        c1 = testing.factory_category(display_priority=10)
        c2 = testing.factory_category(display_priority=5)
        t1 = testing.factory_ticket(category=c1, start_date='2016-11-05')
        t2 = testing.factory_ticket(category=c1, start_date='2016-11-08')
        t3 = testing.factory_ticket(category=c2)
        res = self.client.get(self._getTarget())
        self.assertTemplateUsed(res, 'tickets/list.html')
        self.assertEqual(len(res.context['tickets']), 3)
        self.assertEqual(res.context['tickets'][0], t1)
        self.assertEqual(res.context['tickets'][1], t2)
        self.assertEqual(res.context['tickets'][2], t3)

    def test_get_paginate(self):
        c1 = testing.factory_category(display_priority=10)
        tickets = []
        for i in range(21):
            t = testing.factory_ticket(category=c1, start_date='2016-11-05')
            tickets.append(t)
        res = self.client.get(self._getTarget())
        self.assertTemplateUsed(res, 'tickets/list.html')
        self.assertEqual(len(res.context['tickets']), 20)
        self.assertEqual(list(res.context['tickets']), tickets[:20])

        res = self.client.get(self._getTarget(), data={'page': 2})
        self.assertTemplateUsed(res, 'tickets/list.html')
        self.assertEqual(len(res.context['tickets']), 1)
        self.assertEqual(list(res.context['tickets']), tickets[20:])

    def test_get_paginate_invalid_param(self):
        t1 = testing.factory_ticket()
        res = self.client.get(self._getTarget(), data={'page': '無効'})
        self.assertTemplateUsed(res, 'tickets/list.html')
        self.assertEqual(len(res.context['tickets']), 1)
        self.assertEqual(res.context['tickets'][0], t1)

    def test_get_paginate_too_big_page(self):
        t1 = testing.factory_ticket()
        res = self.client.get(self._getTarget(), data={'page': 999999})
        self.assertTemplateUsed(res, 'tickets/list.html')
        self.assertEqual(len(res.context['tickets']), 1)
        self.assertEqual(res.context['tickets'][0], t1)


class TestTicketDetail(TestCase):
    def _getTarget(self, **kwargs):
        return reverse('tickets:detail', kwargs=kwargs)

    def setUp(self):
        self.user = factory_user()
        self.client.force_login(self.user)

    def test_get(self):
        t = testing.factory_ticket()
        res = self.client.get(self._getTarget(ticket_id=t.id))
        self.assertTemplateUsed(res, 'tickets/detail.html')
        self.assertEqual(res.context['ticket'], t)
        self.assertEqual(res.context['form'].ticket, t)

    def test_get_sold_out(self):
        t = testing.factory_ticket(status=models.Ticket.STATUS_SOLD_OUT)
        res = self.client.get(self._getTarget(ticket_id=t.id))
        self.assertEqual(res.status_code, 404)

    def test_post(self):
        t = testing.factory_ticket(quantity=50)
        res = self.client.post(self._getTarget(ticket_id=t.id),
                               data={'amount': 50})
        self.assertRedirects(res, reverse('tickets:list'))
        self.assertEqual(len(self.client.session['cart']), 1)
        self.assertEqual(self.client.session['cart'][0]['ticket_id'], t.id)
        self.assertEqual(self.client.session['cart'][0]['amount'], 50)

    def test_post_invalid(self):
        t = testing.factory_ticket(quantity=50)
        res = self.client.post(self._getTarget(ticket_id=t.id),
                               data={'amount': 51})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.context['form'].errors['amount'],
                         ['在庫が不足しています'])


class TestTicketManage(TestCase):
    def _getTarget(self, **kwargs):
        # return reverse('tickets:manage', kwargs=kwargs)
        pass

    def setUp(self):
        self.user = factory_user()
        self.client.force_login(self.user)

    def test_get(self):
        t = testing.factory_ticket(seller=self.user)
        res = self.client.get(self._getTarget(ticket_id=t.id))
        self.assertTemplateUsed(res, 'tickets/manage.html')
        self.assertEqual(res.context['ticket'], t)
    def test_get_not_my_ticket(self):
        t = testing.factory_ticket(seller=factory_user())
        res = self.client.get(self._getTarget(ticket_id=t.id))
        self.assertEqual(res.status_code, 404)
    def test_get_sold_out_ticket(self):
        t = testing.factory_ticket(seller=self.user,
                                    status=models.Ticket.STATUS_SOLD_OUT)
        res = self.client.get(self._getTarget(ticket_id=t.id))
        self.assertEqual(res.status_code, 404)
    def test_post(self):
        t = testing.factory_ticket(seller=self.user,
                                   status=models.Ticket.STATUS_DISPLAY)
        res = self.client.post(self._getTarget(ticket_id=t.id))
        self.assertRedirects(res, reverse('tbpauth:mypage'))
        t.refresh_from_db()
        self.assertEqual(t.status, models.Ticket.STATUS_STOPPED)


class TestTicketSell(TestCase):
    def _getTarget(self):
        return reverse('tickets:sell')
        

    def setUp(self):
        self.user = factory_user()
        self.client.force_login(self.user)

    def test_get(self):
        res = self.client.get(self._getTarget())
        self.assertTemplateUsed(res, 'tickets/sell.html')
        self.assertIn('form', res.context)
    def test_post_invalid(self):
        res = self.client.post(
            self._getTarget(),
            data={
                'name':'チケット名',
                'start_date': '2016-11-16',
                'price': 120,
                'quantity': 100,
            }
        )
        self.assertTemplateUsed(res, 'tickets/sell.html')
        self.assertEqual(res.context['form'].errors['price'],
                         ['100 ごとの値を入力してください (入力は 120)。'])
        
                         

    def test_post_confirm(self):
        res = self.client.post(
            self._getTarget(),
            data={
                'name': 'チケット名',
                'start_date': '2016-11-16',
                'price': 100,
                'quantity': 100,
                }
        )
        self.assertTemplateUsed(res, 'tickets/sell_confirm.html')
        self.assertEqual(res.context['ticket'].name, 'チケット名')
        self.assertEqual(res.context['ticket'].start_date.isoformat(), '2016-11-16')
        self.assertEqual(res.context['ticket'].price, 100)
        self.assertEqual(res.context['ticket'].quantity, 100)
        self.assertEqual(res.context['ticket'].fee(), 1)       

    def test_post_confirm_invalid(self):
        res = self.client.post(
            self._getTarget(),
            data={
                'name': 'チケット名',
                'start_date': '2016-11-16',
                'price': 120,
                'quantity': 100,
                'confirmed': '1',
            }
        )
        self.assertTemplateUsed(res, 'tickets/sell.html')
        self.assertEqual(res.context['form'].errors['price'],
                         ['100 ごとの値を入力してください (入力は 120)。'])

    def test_post_confirm_success(self):
        res = self.client.post(
            self._getTarget(),
            data={
                'name': 'チケット名',
                'start_date': '2016-11-16',
                'price': 100,
                'quantity': 100,
                'confirmed': '1',
            }
        )
        self.assertEqual(res.status_code, 302)

        self.assertEqual(models.Ticket.objects.count(), 1)
        t = models.Ticket.objects.first()
        self.assertEqual(t.name, 'チケット名')
        self.assertEqual(t.seller, self.user)
        self.assertEqual(t.start_date.isoformat(), '2016-11-16')
        self.assertEqual(t.price, 100)
        self.assertEqual(t.quantity, 100)

        self.assertRedirects(res, reverse('tickets:manage', kwargs={'ticket_id': t.id}))
