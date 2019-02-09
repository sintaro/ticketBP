from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.template.response import TemplateResponse

from . import forms

@login_required
def mypage(request):
    """ マイページ画面
    """
    purchases = request.user.purchases.order_by('bought_at')
    #ユーザーでpermission
    selling_tickets = request.user.selling_tickets.order_by('status', 'start_date')
    #ユーザーでpermission
    #offering_tickets =
    return TemplateResponse(request, 'tbpauth/mypage.html',
                            {'profile_user': request.user,
                             'purchases': purchases,
                            'selling_tickets': selling_tickets})


@login_required
def mypage_edit(request):
    """ マイページ編集・更新画面
    """
    if request.method == 'POST':
        form = forms.ProfileEditForm(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('tbpauth:mypage')
    else:
        form = forms.ProfileEditForm(instance=request.user)
    return TemplateResponse(request, 'tbpauth/edit.html',
                            {'form': form})
                                