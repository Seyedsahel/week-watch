from zoneinfo import available_timezones
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
    can_save = models.BooleanField(default=True) 

    def __str__(self):
        return self.domain
#-----------------------------------------------------
class UnScraped(models.Model):
    link = models.CharField(max_length=200)
    execption_name = models.CharField(max_length=100)
    execption_text = models.TextField()


    def __str__(self):
        return f"{self.link}  {self.execption_name}"

    @staticmethod
    def report_website(website_link,exception,description=""):
        try:
            obj = UnScraped.objects.get(link=website_link, execption_name=exception, execption_text=description)
        except UnScraped.DoesNotExist:
            obj = UnScraped.objects.create(link=website_link, execption_name=exception, execption_text=description)
        return obj
#-----------------------------------------------------