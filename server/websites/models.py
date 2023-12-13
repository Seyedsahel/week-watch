from django.db import models
#-----------------------------------------------------
class WebSiteCategory(models.Model):
    name = models.CharField(max_length=100)


    def __str__(self):
        return self.name
#-----------------------------------------------------
class Website(models.Model):
    domain = models.CharField(unique=True,max_length=100)
    categories = models.ManyToManyField(WebSiteCategory,related_name="websites")

    def __str__(self):
        return self.domain
#-----------------------------------------------------
