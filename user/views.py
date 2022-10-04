from django.shortcuts import render, redirect
from .models import UserModel
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib import auth
from django.contrib.auth.decorators import login_required

# Create your views here.
def sign_up_view(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect('/')
        else:
            return render(request, 'user/signup.html')
    elif request.method == 'POST':
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        password2 = request.POST.get('password2','')
        first_name = request.POST.get('first_name','')
        
        if password != password2:
            return render(request, 'user/signup.html',{'error':'패스워드를 확인 해 주세요!'})
        else:
            if username == '' or password == '':
                return render(request, 'user/signup.html',{'error':'사용자 이름과 비밀번호는 필수 값 입니다.'})
            
            exist_user = get_user_model().objects.filter(username=username)   
            if exist_user:
                return render(request, 'user/signup.html',{'error':'사용자가 존재합니다.'})
            else:
                UserModel.objects.create_user(username=username, password=password, first_name=first_name)
                return redirect('/sign-in')


def sign_in_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        
        me = auth.authenticate(request, username=username, password=password)
        if me is not None:
            auth.login(request, me)
            return redirect('/')
        else:
            return render(request,'user/signin.html',{'error':'유저이름 혹은 패스워드를 확인 해 주세요'})
        
    elif request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect('/')
        else:
            return render(request, 'user/signin.html')

@login_required        
def logout(request):
    auth.logout(request)
    return redirect('/')

# user/views.py 

@login_required
def user_view(request):
    if request.method == 'GET':
        # 사용자를 불러오기, exclude와 request.user.username 를 사용해서 '로그인 한 사용자'를 제외하기
        user_list = UserModel.objects.all().exclude(username=request.user.username)
        return render(request, 'user/user_list.html', {'user_list': user_list})
    else:
        return render(request, 'user/user_list.html')


@login_required
def user_follow(request, id):
    me = request.user
    click_user = UserModel.objects.get(id=id)
    if me in click_user.followee.all():
        click_user.followee.remove(request.user)
    else:
        click_user.followee.add(request.user)
    return redirect('/user')

# @login_required
def profile(request):
    return render(request, 'user/profile.html')

def change_profile(request):
    if request.method == 'POST':
        user_image = request.user
        print(user_image)
        print(request.FILES)
        user_image.image = request.FILES.get('image','')
        user_image.save()

        return render(request, 'user/profile.html')
            
    elif request.method == 'GET':
        user_image = UserModel()
        return render(request, 'user/change_profile.html',{'image':user_image})

def profile_change(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect('/')
        else:
            return render(request, 'user/profile.html')
    elif request.method == 'POST':
        username = request.POST.get('username','')
        first_name = request.POST.get('first_name','')
        bio = request.bio.POST.get('post','')
        # email = request.POST.get('email','')
        # phone = request.POST.get('phone','')
        # gender = request.POST.get('gender','')
        
