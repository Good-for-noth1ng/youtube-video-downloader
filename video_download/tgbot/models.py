from __future__ import annotations
from typing import Union, Optional, Tuple

from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Manager, QuerySet
from telegram import Update
from telegram.ext import CallbackContext

from video_download.settings import DEBUG
from tgbot.handlers.utils.info import extract_user_data_from_update

nb = dict(null=True, blank=True)


class CreateTracker(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        abstract = True
        ordering = ('-created_at',)


class CreateUpdateTracker(CreateTracker):
    updated_at = models.DateTimeField(auto_now=True)

    class Meta(CreateTracker.Meta):
        abstract = True


class GetOrNoneManager(models.Manager):
    """returns none if object doesn't exist else model instance"""
    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except ObjectDoesNotExist:
            return None

class AdminUserManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_admin=True)

class User(CreateUpdateTracker):
    user_id = models.PositiveIntegerField(primary_key=True)
    user_name = models.CharField(max_length=32, **nb)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256, **nb)
    deep_link = models.CharField(max_length=64, **nb)
    is_blocked_bot = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = GetOrNoneManager()
    admins = AdminUserManager()


    def __str__(self):
        return f"@{self.user_name}" if self.user_name is not None else f"{self.user_id}"


    @classmethod
    def get_user_and_created(cls, update: Update, context: CallbackContext) -> Tuple[User, bool]:
        """Create user and put into db if user exists, returns User object and creation status"""
        data = extract_user_data_from_update(update)
        u, created = cls.objects.update_or_create(user_id=data["user_id"], defaults=data)
        if created:
            if context is not None and context.args is not None and len(context.args) > 0:
                payload = context.args[0]
                if str(payload).strip() != str(data["user_id"]).strip():  # you can't invite yourself
                    u.deep_link = payload
                    u.save()
        return u, created

    @classmethod
    def get_user(cls, update: Update, context: CallbackContext) -> User:
        """Gets user from db"""
        u, _ = cls.get_user_and_created(update, context)
        return u

    @classmethod
    def get_user_by_username_or_user_id(cls, username_or_user_id: Union[str, int]) -> Optional[User]:
        """ Search user in DB, return User or None if not found """
        username = str(username_or_user_id).replace("@", "").strip().lower()
        if username.isdigit():  # user_id
            return cls.objects.filter(user_id=int(username)).first()
        return cls.objects.filter(username__iexact=username).first()

    @property
    def invited_users(self) -> QuerySet[User]:
        return User.objects.filter(deep_link=str(self.user_id), created_at__gt=self.created_at)

    @property
    def tg_str(self) -> str:
        if self.user_name:
            return f'@{self.user_name}'
        return f"{self.first_name} {self.last_name}" if self.last_name else f"{self.first_name}"

    @property
    def get_user_id(self):
        return self.user_id

