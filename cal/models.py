from django.db import models
from django.urls import reverse

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    

    @property
    def get_html_url(self):
        url = reverse('cal:event_edit', args=(self.id,))
        return f'<a href"{url}"> {self.title} </a>'

class Email(models.Model):
    to = models.EmailField(max_length=254)
    message = models.TextField(max_length=4500)

    def __str__(self):
        return self.to