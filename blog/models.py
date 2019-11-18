from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User #one to many relationship
from django.urls import reverse
from PIL import Image
from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta as tdelta

class Post(models.Model):
    title = models.CharField(max_length = 100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author  = models.ForeignKey(User,on_delete=models.CASCADE)
    image = models.ImageField(blank=True,null=True,upload_to='posts_pics')
    positive_votes = models.IntegerField(default=0)
    negative_votes = models.IntegerField(default=0)
    total_points = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.username} Profile'
    
    @property
    def image_url(self):
        if self.image:
            img = Image.open(self.image.path)

            if img.height > 600 or img.width > 600:
                output_size = (400,300)
                img.save(self.image.path)


            return self.image.url
        return ''

    def save(self):
        super().save()

    def __str__(self):
        return f'{self.user.username} Profile'

    def __str__(self): #magic methods ?
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail',kwargs={'pk':self.pk})

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)

class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)#try True here

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text

