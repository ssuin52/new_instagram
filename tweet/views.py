from re import T
from urllib import request
from django.shortcuts import render, redirect
from .models import TweetModel
from .models  import TweetComment
from user.models import UserModel
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, TemplateView
import random

# Create your views here.

def home(request):
    user = request.user.is_authenticated
    if user:
        return redirect('/tweet')
    else:
        return redirect('/sign-in')
    
def tweet (request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        
        if user:
            all_tweet = TweetModel.objects.all().order_by('-created_at')
            all_comment = TweetComment.objects.all().order_by('-created_at')
            all_image = TweetComment.objects.all().order_by('-created_at')
            profile_image = TweetModel.objects.all()
            recommend_list = UserModel.objects.all().exclude(username=request.user.username).order_by('id')[:5]
            return render(request, 'tweet/home.html',{'tweet':all_tweet ,'comment':all_comment, 'image':all_image, 'recommend_list': recommend_list, 'profile_image' : profile_image})
        else:
            return redirect('/sign-in')
        
    elif request.method == 'POST':
        user = request.user
        content = request.POST.get('my-content')
        tags = request.POST.get('tag','').split(',')
        profile_image = request.FILES.get('profile_image', '')
        image = request.FILES.get('image', '')
        
        if content == '':
            all_tweet = TweetModel.objects.all().order_by('-created_at')
            return render(request,'tweet/post-add.html',{'error':'글은 공백일 수 없습니다.','tweet':all_tweet})
        else:
            my_tweet = TweetModel.objects.create(author=user, content=content, image=image, profile=profile_image)
            for tag in tags:
                tag = tag.strip()
                if tag != '':
                    my_tweet.tags.add(tag)
            my_tweet.save()
            return redirect('/tweet')

@login_required
def detail_tweet(request, id):
    my_tweet = TweetModel.objects.get(id=id)
    tweet_comment = TweetComment.objects.filter(tweet_id=id).order_by('-created_at')
    return render(request,'tweet/tweet_detail.html',{'tweet':my_tweet,'comment':tweet_comment})


@login_required
def write_comment(request, id):
    if request.method == 'POST':
        comment = request.POST.get("comment","")
        current_tweet = TweetModel.objects.get(id=id)

        TC = TweetComment()
        TC.comment = comment
        TC.author = request.user
        TC.tweet = current_tweet
        TC.save()

        return redirect('/tweet/'+str(id))
    
@login_required
def delete_comment(request, id):
    comment = TweetComment.objects.get(id=id)
    current_tweet = comment.tweet.id
    comment.delete()
    return redirect('/tweet/'+str(current_tweet))
    
@login_required
def delete_tweet(request,id):
    my_tweet = TweetModel.objects.get(id=id)
    my_tweet.delete()
    return redirect('/tweet')

class TagCloudTV(TemplateView):
    template_name = 'taggit/tag_cloud_view.html'


class TaggedObjectLV(ListView):
    template_name = 'taggit/tag_with_post.html'
    model = TweetModel

    def get_queryset(self):
        return TweetModel.objects.filter(tags__name=self.kwargs.get('tag'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tagname'] = self.kwargs['tag']
        return context
    
def post_add(request):
    return render(request, 'tweet/post-add.html') 

def post_edit(request):
    return render(request, 'tweet/post-edit.html')

@login_required
def recommend_view(request):
    if request.method == 'GET':
        # 사용자를 불러오기, exclude와 request.user.username 를 사용해서 '로그인 한 사용자'를 제외하기
        recommend_list = UserModel.objects.all().exclude(username=request.user.username)
        return render(request, 'tweet/home.html', {'recommend_list': recommend_list})
    
@login_required
def user_follow(request, id):
    me = request.user
    click_user = UserModel.objects.get(id=id)
    if me in click_user.followee.all():
        click_user.followee.remove(request.user)
    else:
        click_user.followee.add(request.user)
    return redirect('/tweet')

