from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from django.shortcuts import redirect
from .forms import ProfileEditForm
from purchase.models import Purchase
from tickets.models import Ticket

@login_required
def mypage(request):
    """ �}�C�y�[�W���
    """
    # �w���������擾���鏈����ǉ�����
    # ���я��� �w���� �� �Â��� �ł�
    # purchase/models.py �� Purchase ���f����\�����Ă�������
    purchases = Purchase.objects.filter(user=request.user).order_by('bought_at')
    
    # �o�i�������擾����
    sells = Ticket.objects.filter(seller=request.user).order_by('status','-created_at')
    
    # �w�������Əo�i�����̃f�[�^��n����mypage�ɕ\������
    return TemplateResponse(request, 'tbpauth/mypage.html',
                            {'profile_user': request.user,
                             'purchases': purchases,
                             'sells': sells})

@login_required
def mypage_edit(request):
    """ �}�C�y�[�W�ҏW�E�X�V���
    """
    # POST�̏ꍇ�͓��͓��e��ۑ�����
    if request.method == 'POST':
        form = ProfileEditForm(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('tbpauth:mypage')
    else:
        # �o���f�[�V�����Ɏ��s���邩GET�Ȃ�
        form = ProfileEditForm(instance=request.user)
    return TemplateResponse(request, 'tbpauth/edit.html',
                           {'form':form})