from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse


@login_required
def mypage(request):
    """ マイページ画面
    """
    return TemplateResponse(request, 'tbpauth/mypage.html',
                            {'profile_user': request.user})
