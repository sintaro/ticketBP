from django.test import TestCase
from django.urls import reverse

from tbpauth.testing import factory_user
from purchase.testing import factory_purchase
from tickets.models import Ticket
from tickets.testing import factory_ticket

class TestMyPage(TestCase):
    def _getTarget(self):
        return reverse('tbpauth:mypage')

    def setUp(self):
        self.user = factory_user()
        self.client.force_login(self.user)

    def test_get(self):
        p = factory_purchase(user=self.user)
        p2 = factory_purchase(user=self.user)
        t3 = factory_ticket(seller=self.user, status=Ticket.STATUS_STOPPED,
                    start_date='2016-12-01')
        t2 = factory_ticket(seller=self.user, status=Ticket.STATUS_STOPPED,
                    start_date='2016-11-30')
        t1 = factory_ticket(seller=self.user, status=Ticket.STATUS_DISPLAY)  
        res = self.client.get(self._getTarget())
        self.assertEqual(len(res.context['purchases']), 2)
        self.assertTemplateUsed(res, 'tbpauth/mypage.html')
        self.assertEqual(res.context['profile_user'], self.user)
        self.assertEqual(res.context['purchases'][0], p)
        self.assertEqual(res.context['purchases'][1], p2)
        self.assertEqual(len(res.context['selling_tickets']), 3)
        self.assertEqual(res.context['selling_tickets'][0], t1)
        self.assertEqual(res.context['selling_tickets'][1], t2)
        self.assertEqual(res.context['selling_tickets'][2], t3)
class TestMyPageEdit(TestCase):
    def _getTarget(self):
        return reverse('tbpauth:mypage_edit')

    def setUp(self):
        self.user = factory_user()
        self.client.force_login(self.user)

    def test_get(self):
        res = self.client.get(self._getTarget())
        self.assertTemplateUsed(res, 'tbpauth/edit.html')
        self.assertEqual(res.context['form'].instance, self.user)
        
    def test_post(self):
        res = self.client.post(self._getTarget(),
                               data={
                                   'last_name': '鈴木',
                                   'first_name': '里見',
                                    'address1': '埼玉県',
                                   'address2': 'サイタマーマンション',
                               })
        self.assertRedirects(res, reverse('tbpauth:mypage'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.last_name, '鈴木')
        self.assertEqual(self.user.first_name, '里見')
        self.assertEqual(self.user.address1, '埼玉県')
        self.assertEqual(self.user.address2, 'サイタマーマンション')
                                      
                                   
    def test_post_invalid(self):
        res = self.client.post(self._getTarget(),
                               data={
                                   'last_name': '',
                                   'first_name': '里見',
                                    'address1': '埼玉県',
                                   'address2': 'サイタマーマンション',
                               })
        self.assertTemplateUsed(res, 'tbpauth/edit.html')
        self.assertEqual(res.context['form'].errors['last_name'],
                      ['このフィールドは必須です。'])    
        
                                   
                                   
                               
