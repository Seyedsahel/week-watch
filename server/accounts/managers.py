from django.contrib.auth.models import BaseUserManager


class MyUserManager(BaseUserManager):
    def create_user(self,email,password):
        if not email:
            raise ValueError('users must have email')

        user = self.model(email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,password):
        user = self.create_user(email,password)
        user.is_admin = True
        user.save(using=self._db)
        return user