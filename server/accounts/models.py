from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import MyUserManager
#-----------------------------------------------------
class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='media/users/%Y/%m/')
    can_change_password = models.BooleanField(default=False)
    code = models.IntegerField(blank=True,null=True)




    USERNAME_FIELD = 'email'
    objects = MyUserManager()

    def __str__(self):
        return str(self.email) + " - " + str(self.full_name) + " - " + str(self.id)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
#-----------------------------------------------------