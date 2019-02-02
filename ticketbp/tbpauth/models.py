from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
import uuid as uuid_lib

class Department(models.Model):
    """所属 兼任可"""

    name = models.CharField(_('所属'), max_length=150, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('所属')
        verbose_name_plural = _('所属')


class User(AbstractBaseUser, PermissionsMixin):
    """ユーザー AbstractUserをコピペし編集"""
    address1 = models.CharField("住所1", max_length=32, blank=True, null=True)
    address2 = models.CharField("住所2", max_length=128, blank=True, null=True)


    uuid = models.UUIDField(default=uuid_lib.uuid4,
                            primary_key=True, editable=False)
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_(
            '必須項目です。150文字以内で数字と @/./+/-/_ が使えます'),
        validators=[username_validator],
        error_messages={
            'unique': _("そのユーザ名は既に使用されています。別のユーザー名をお試し下さい。"),
        },
    )
    full_name = models.CharField(_('氏名'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), blank=True)
    departments = models.ManyToManyField(
        Department,
        verbose_name=_('所属'),
        blank=True,
        help_text=_('このユーザーの所属があれば記載ください'),
        related_name="user_set",
        related_query_name="user",
    )

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', ]

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    # 既存メソッドの変更
    def get_full_name(self):
        return self.username
