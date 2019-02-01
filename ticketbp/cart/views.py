from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.views.decorators.http import require_POST

from tickets.models import Ticket

@login_required
def cart_list(request):
    """ カート一覧・注文画面
    """
    if request.method == 'POST':
        if request.cart.num_items() == 0:
            error = 'カートが空です'
        elif not request.cart.check_stock():
            error = '在庫が不足しています'
        else:
             total_price_display = request.cart.total_price_display()
             request.cart.purchase(request.user)
             return TemplateResponse(request, 'cart/thanks.html',
                                     {'total_price_display': total_price_display})
    else:
        error = None
    return TemplateResponse(request, 'cart/list.html', {'cart': request.cart,
                                                        'error': error})


@require_POST
@login_required
def cart_delete(request, ticket_id):
    """ カートからチケットを削除する
    POST用のView
    """
    ticket = get_object_or_404(Ticket, id=ticket_id)
    request.cart.delete_ticket(ticket)
    return redirect('cart:list')