from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse

from . import forms
from . import models


def ticket_list(request):
    """ �`�P�b�g�ꗗ���
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
    """ �`�P�b�g�ڍ׉��
    * �o�i�҈ȊO�̃��[�U�[ => �J�[�g�ɒǉ�
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
    """ �`�P�b�g�ҏW (�o�i��~) �y�[�W
    """
    # �Ƃ肠�����`�P�b�g�̏��͎擾
    ticket = get_object_or_404(models.Ticket, id=ticket_id, seller=request.user,
	                               status=models.Ticket.STATUS_DISPLAY)        
    if request.method == 'POST':
        # POST�̏ꍇ�A�Ώۂ̃`�P�b�g�̃X�^�[�^�X���o�i��~�ɕύX���ĕۑ�����
        ticket.status = models.Ticket.STATUS_STOPPED
        ticket.save()
        return redirect('tbpauth:mypage')
    
    return TemplateResponse(request, 'tickets/manage.html',
                           {'ticket':ticket})


@login_required
def ticket_sell(request):
    """ �`�P�b�g�o�i��ʁE�m�F��ʁE�o�i
    """
    # ���\�b�h�� GET �̏ꍇ�� TicketSellingForm ��\���i�e���v���[�g�� tickets/sell.html �j
    # 1�x�ڂ� POST �œ��͂��������ꍇ�A�m�F��ʂƃt�H�[�����ēx�\���i�e���v���[�g�� tickets/sell_confirm.html�j
    # �m�F��ʂ����2�x�ڂ� POST �œ��͂��������ꍇ�A�`�P�b�g���쐬���܂�

    # POST��1�x�ڂ�2�x�ڂ��͂ǂ�����Ĕ��f����΂����H
    # �m�F���tickets/sell_confirm.html���痈�Ă����2��ڂ̂͂�
    # confirm.html�ɂ�
    # <input type="hidden" name="confirmed" value="1">�Ƃ���悤��
    # confirmed�̉B���v�f������̂ł���Ŕ��肷��
    
    if request.method == 'POST':
        if 'confirmed' in request.POST:
            # 2��ڂ̏ꍇ�͏o�i����`�P�b�g���쐬����
            form = forms.TicketSellingForm(request.POST)
            if form.is_valid():
                ticket = form.save(commit=False)               
                ticket.seller = request.user
                ticket.save()
                return redirect('tickets:manage', ticket_id = ticket.id)
        else:
            # 1��ڂ̏ꍇ�͊m�F��ʂƃt�H�[�����ēx�\��
            form = forms.TicketSellingForm(request.POST)
            if form.is_valid():
                ticket = form.save(commit=False)
                return TemplateResponse(request,'tickets/sell_confirm.html',
                                       {'form':form,
                                        'ticket':ticket})
    else:
        # GET�̏ꍇ��o���f�[�V�����Ɏ��s�����ꍇ��TicketSellingForm��\��
        form = forms.TicketSellingForm()
        
    return TemplateResponse(request, 'tickets/sell.html',
                               {'form': form})
    