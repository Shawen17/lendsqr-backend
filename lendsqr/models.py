from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime,date
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .managers import UserManager
from django.utils import timezone
from django.contrib.auth.models import Group, Permission



class User(AbstractUser):
    username= None
    email=models.EmailField(_('email address'),unique=True)
    state=models.CharField(max_length=50,default='Lagos')


    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        related_name='%(class)s_groups'  # Custom related_name for groups
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name='%(class)s_user_permissions'  # Custom related_name for user_permissions
    )
    

    class Meta:
        verbose_name=_('user')
        verbose_name_plural=_('users')

    objects=UserManager()

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['first_name','last_name','state','password']

    def __str__(self):
        return self.email


    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        return self.first_name