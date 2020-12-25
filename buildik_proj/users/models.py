from django.contrib.auth.models import AbstractUser
from django.db import models
from social_django.models import UserSocialAuth


class User(AbstractUser):
    def to_json(self):
        jsoned_user = {field.name: getattr(self, field.name) for field in User._meta.fields}
        jsoned_user.pop('password')
        return jsoned_user

    def to_representation(self):
        jsoned_user = {field.name.replace("_", " ").capitalize(): getattr(self, field.name) for field in User._meta.fields}
        jsoned_user.pop('Password')
        jsoned_user.pop('Id')
        return jsoned_user
    
    def isSocial(self):
        try:
            UserSocialAuth.objects.get(user_id=self.id)
        except UserSocialAuth.DoesNotExist:
            return False
        else:
            return True
