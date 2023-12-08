from django.db import models
from accounts.models import User
#-----------------------------------------------------
class WebSiteCategory(models.Model):
    name = models.CharField(max_length=100)


    def __str__(self):
        return self.domain
#-----------------------------------------------------
class Website(models.Model):
    domain = models.URLField(unique=True)
    category = models.ForeignKey(WebSiteCategory,null=True,blank=True,on_delete=models.CASCADE,related_name="websites")
    

    def __str__(self):
        return self.domain
#-----------------------------------------------------
class HistoryRecord(models.Model):
    link = models.CharField(max_length=100)
    website = models.ForeignKey(Website,null=True,blank=True,on_delete=models.CASCADE,related_name="records")
    user = models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE,related_name="records")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        formatted_date = self.created.strftime("%d %H:%M:%S")
        return f"{self.user.email} - {self.website.domain} - {formatted_date}"

#-----------------------------------------------------




