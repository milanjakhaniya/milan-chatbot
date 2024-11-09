from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Message(models.Model):
    id = models.AutoField(primary_key=True)
    task_id = models.CharField(max_length=255, unique=True) 
    query = models.TextField()
    query_response = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_by_user')
    last_modified_on = models.DateTimeField(auto_now=True)
    last_modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='last_modified_by_user')

    def __str__(self):
        return f"{self.task_id}"  

    class Meta:
        db_table = 'Message'