# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Tag(models.Model):
 tag = models.CharField('タグ名', max_length=50)
 def __str__(self):
   return self.tag
class Post(models.Model):
   title = models.CharField('タイトル', max_length=35)
   text = models.TextField('本文')
   image = models.ImageField('クラス図', upload_to = 'images', blank=True)
   code = models.FileField('plantuml', upload_to = 'plantuml', blank=True)
   created_at = models.DateTimeField('投稿日', default=timezone.now)
   tag = models.ForeignKey(Tag, verbose_name = 'タグ', on_delete=models.PROTECT)
   user = models.ForeignKey(User, on_delete=models.CASCADE)

   def __str__(self):
       return self.title
   def file_name(self):
       path = os.path.basename(self.code.name)
       return path