from django.db import models
from accounts.models import User
from websites.models import Website
from django.utils.timezone import make_aware
#-----------------------------------------------------
class HistoryRecord(models.Model):
    link = models.CharField(max_length=300)
    website = models.ForeignKey(Website,null=True,blank=True,on_delete=models.CASCADE,related_name="records")
    user = models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE,related_name="records")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    closed = models.DateTimeField(null=True, blank=True)
    next_record = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name="previous_records")

    def __str__(self):
        formatted_date = self.created.strftime("%d %H:%M:%S")
        return f"{self.user.email} - {self.website.domain} - {formatted_date}"

    def clean(self):
        super().clean()
        self.closed = make_aware(self.closed)
#-----------------------------------------------------




