from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse

from . import forms
from . import models

def ticket_list(request):
    """ チケット一覧画面
    """
    tickets = models.Ticket.objects.select_related('category').filter(
        status=models.Ticket.STATUS_DISPLAY,
    ).order_by('-category__display_priority', 'start_date')
    
    paginator = Paginator(tickets, per_page=20)
    page = request.GET.get('page')
    
    try:
        tickets = paginator.page(page)
    except (EmptyPage,PageNotAnInteger):
        tickets = paginator.page(1)
    return TemplateResponse(request, 'tickets/list.html',{'tickets':tickets})


@login_required
def ticket_detail(request, ticket_id):
    """ チケット詳細画面
    * 出品者以外のユーザー => カートに追加
    """
    ticket = get_object_or_404(models.Ticket, id=ticket_id, status=models.Ticket.STATUS_DISPLAY)
    if request.method == 'POST':
        form = forms.TicketCartForm(ticket=ticket, data=request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            request.cart.add_ticket(ticket, amount)
            return redirect('tickets:list')
    else:
        form = forms.TicketCartForm(ticket=ticket)
        
    return TemplateResponse(request, 'tickets/detail.html', {'ticket': ticket, 'form': form})
