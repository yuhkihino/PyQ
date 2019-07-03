from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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
    ).order_by('-category.display_priority', 'start_date')
    paginator = Paginator(tickets, per_page=20)

    page = request.GET.get('page')
    try:
        tickets = paginator.page(page)
    except (EmptyPage, PageNotAnInteger):
        tickets = paginator.page(1)
    return TemplateResponse(request, 'tickets/list.html', {'tickets': tickets})


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
    # とりあえずチケットの情報は取得
    ticket = get_object_or_404(models.Ticket, id=ticket_id, seller=request.user,
	                               status=models.Ticket.STATUS_DISPLAY)        
    if request.method == 'POST':
        # POSTの場合、対象のチケットのスタータスを出品停止に変更して保存する
        ticket.status = models.Ticket.STATUS_STOPPED
        ticket.save()
        return redirect('tbpauth:mypage')
    
    return TemplateResponse(request, 'tickets/manage.html',
                           {'ticket':ticket})


@login_required
def ticket_sell(request):
    """ チケット出品画面・確認画面・出品
    """
    # メソッドが GET の場合は TicketSellingForm を表示（テンプレートは tickets/sell.html ）
    # 1度目の POST で入力が正しい場合、確認画面とフォームを再度表示（テンプレートは tickets/sell_confirm.html）
    # 確認画面からの2度目の POST で入力が正しい場合、チケットを作成します

    # POSTが1度目か2度目かはどうやって判断すればいい？
    # 確認画面tickets/sell_confirm.htmlから来ていれば2回目のはず
    # confirm.htmlには
    # <input type="hidden" name="confirmed" value="1">とあるように
    # confirmedの隠し要素があるのでこれで判定する
    
    if request.method == 'POST':
        if 'confirmed' in request.POST:
            # 2回目の場合は出品するチケットを作成する
            form = forms.TicketSellingForm(request.POST)
            if form.is_valid():
                ticket = form.save(commit=False)               
                ticket.seller = request.user
                ticket.save()
                return redirect('tickets:manage', ticket_id = ticket.id)
        else:
            # 1回目の場合は確認画面とフォームを再度表示
            form = forms.TicketSellingForm(request.POST)
            if form.is_valid():
                ticket = form.save(commit=False)
                return TemplateResponse(request,'tickets/sell_confirm.html',
                                       {'form':form,
                                        'ticket':ticket})
    else:
        # GETの場合やバリデーションに失敗した場合はTicketSellingFormを表示
        form = forms.TicketSellingForm()
        
    return TemplateResponse(request, 'tickets/sell.html',
                               {'form': form})
    