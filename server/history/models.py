from django.db import models
from accounts.models import User
from websites.models import Website
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




