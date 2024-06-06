from django.db import models
from django.contrib.auth.models import User
import shortuuid
import os

class ChatGroup(models.Model):
    group_name = models.CharField(max_length=128, unique=True,default=shortuuid.uuid)
    groupchat_name = models.CharField(max_length=128, null=True, blank=True)
    admin = models.ForeignKey(User, on_delete=models.SET_NULL,related_name="groupchats",blank=True,null=True)
    users_online = models.ManyToManyField(User, blank=True,related_name='online_in_groups')
    members = models.ManyToManyField(User, blank=True,related_name='chat_groups')
    is_private = models.BooleanField(default=False)
    
    def __str__(self):
        return self.group_name
    
    
class GroupMessage(models.Model):
    group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE,related_name='chat_messages')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.CharField(max_length=300)
    file = models.FileField(null=True, blank=True,upload_to='files/')
    created = models.DateTimeField(auto_now_add=True)
    
    @property
    def filename(self):
        if self.file:
            return os.path.basename(self.file.name)
        
        else:
            return None
    
    def __str__(self):
        if self.body:
            return f"{self.author.username} : {self.body}"

        elif self.file:
            return f"{self.author.username} : {self.file}"
    
    class Meta:
        ordering = ['-created']
        
    @property
    def is_image(self):
        if self.filename.lower().endswith(('.png','.jpg','.jpeg','.gif','.svg','.webp','.avif')):
            return True
        else:
            return False