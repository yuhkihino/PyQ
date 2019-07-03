from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from django.shortcuts import redirect
from .forms import ProfileEditForm
from purchase.models import Purchase
from tickets.models import Ticket

@login_required
def mypage(request):
    """ マイページ画面
    """
    # 購入履歴を取得する処理を追加する
    # 並び順は 購入日 が 古い順 です
    # purchase/models.py の Purchase モデルを表示してください
    purchases = Purchase.objects.filter(user=request.user).order_by('bought_at')
    
    # 出品履歴も取得する
    sells = Ticket.objects.filter(seller=request.user).order_by('status','-created_at')
    
    # 購入履歴と出品履歴のデータを渡してmypageに表示する
    return TemplateResponse(request, 'tbpauth/mypage.html',
                            {'profile_user': request.user,
                             'purchases': purchases,
                             'sells': sells})

@login_required
def mypage_edit(request):
    """ マイページ編集・更新画面
    """
    # POSTの場合は入力内容を保存する
    if request.method == 'POST':
        form = ProfileEditForm(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('tbpauth:mypage')
    else:
        # バリデーションに失敗するかGETなら
        form = ProfileEditForm(instance=request.user)
    return TemplateResponse(request, 'tbpauth/edit.html',
                           {'form':form})