from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(verbose_name='Контент', null=True, blank=True)
    img = models.ImageField(verbose_name='Фото', upload_to='media/',)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан в')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлен в')
    
    def __str__(self):
        return f'Пост от {self.author}'
    
    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(verbose_name='Комментарий',null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан в')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлен в')
    
    def __str__(self):
        return f'Комментарий к {self.post} от {self.author}'
    
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)
    
