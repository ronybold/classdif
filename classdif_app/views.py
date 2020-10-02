# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Tag
from .forms import PostAddForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
# Create your views here.
def is_valid_q(q):
   return q != '' and q is not None
@login_required
def index(request):
   posts = Post.objects.all().order_by('-created_at')
   title_or_user = request.GET.get('title_or_user')
   date_min = request.GET.get('date_min')
   date_max = request.GET.get('date_max')
   tag = request.GET.get('tag')

   if is_valid_q(title_or_user):
       posts = posts.filter(Q(title__icontains=title_or_user)
                      | Q(user__username__icontains=title_or_user)
                      ).distinct()

   if is_valid_q(date_min):
       posts = posts.filter(created_at__gte=date_min)

   if is_valid_q(date_max):
       posts = posts.filter(created_at__lt=date_max)

   if is_valid_q(tag) and tag != 'タグを選択...':
       posts = posts.filter(tag__tag=tag)
   
   return render(request, 'classdif_app/index.html', 
   {'posts': posts, 'title_or_user': title_or_user , 'date_min': date_min, 'date_max': date_max ,'tag': tag})
def detail(request, post_id):
     post = get_object_or_404(Post, id=post_id)
     return render(request, 'classdif_app/detail.html', {'post': post})
def add(request):
   if request.method == "POST":
      form = PostAddForm(request.POST, request.FILES)
      if form.is_valid():
         post = form.save(commit=False)
         post.user = request.user
         post.save()
         return redirect('classdif_app:index')
   else:
       form = PostAddForm()
   return render(request, 'classdif_app/add.html', {'form': form})
@login_required
def edit(request, post_id):
   post = get_object_or_404(Post, id=post_id)
   if request.method == "POST":
       form = PostAddForm(request.POST, request.FILES, instance=post)
       if form.is_valid():
           form.save()
           return redirect('classdif_app:detail', post_id=post.id)
   else:
       form = PostAddForm(instance=post)
   return render(request, 'classdif_app/edit.html', {'form': form, 'post':post })
@login_required
def delete(request, post_id):
   post = get_object_or_404(Post, id=post_id)
   post.delete()
   return redirect('classdif_app:index')
