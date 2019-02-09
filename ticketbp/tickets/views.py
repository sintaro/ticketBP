from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.contrib import auth

from . import models
from . import forms

def ticket_list(request):
    """ チケット一覧画面
    """
    #返信の件数など表示
    tickets = models.Ticket.objects.select_related('category').filter(
        status=models.Ticket.STATUS_DISPLAY,
    ).order_by('-category.display_priority', 'start_date')


    onayami_tickets = models.OnayamiTicket.objects.order_by('created_at')
    paginator = Paginator(tickets, per_page=20)

    # def post(self, request, pk):
    #     user = auth.get_user(request)
    #     bookmark, created = models.BookmarkTicket.objects.get_or_create(user=user, obj_id=pk)

    #     if not created:
    #         bookmark.delete()

    page = request.GET.get('page')

    try:
        tickets = paginator.page(page)
    except (EmptyPage, PageNotAnInteger):
        tickets = paginator.page(1)
    return TemplateResponse(request, 'tickets/list.html', 
        {'tickets': tickets,'onayami_tickets':onayami_tickets})


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


@login_required
def ticket_manage(request, ticket_id):
    """ チケット編集 (出品停止) ページ
    """
    ticket = get_object_or_404(models.Ticket, id=ticket_id, seller=request.user,
                               status=models.Ticket.STATUS_DISPLAY)
    if request.method == 'POST':
        ticket.status = models.Ticket.STATUS_STOPPED
        ticket.save()
        return redirect('tbpauth:mypage')
    return TemplateResponse(request, 'tickets/manage.html',
                            {'ticket': ticket})
                            


@login_required
def ticket_sell(request):
    """ チケット出品画面・確認画面・出品
    """
    if request.method == 'POST':
        if 'confirmed' in request.POST:
            form = forms.TicketSellingForm(request.POST)
            if form.is_valid():
                ticket = form.save(commit=False)
                ticket.seller = request.user
                ticket.save()
                print("confirm",ticket)
                return redirect('tickets:manage', ticket_id=ticket.id)
        else:
            
            form = forms.TicketSellingForm(request.POST)
            if form.is_valid():
                ticket = form.save(commit=False)
                return TemplateResponse(request, 'tickets/sell_confirm.html',
                                        {'form': form,
                                         'ticket': ticket})
    else:
        form = forms.TicketSellingForm()
                    
    return TemplateResponse(request, 'tickets/sell.html',
                            {'form':form})
                                             
                    
