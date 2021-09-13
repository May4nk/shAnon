from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from .models import Suser,Post,Follow,Comments
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from crypt import crypt
from random import shuffle


def loggin(req):
    if req.user.is_authenticated:
        return redirect('home')
    if req.method=='POST':
        username=req.POST['username']
        password=req.POST['password']
        usr = authenticate(req,username=username,password=password)
        if usr:
            print(True)
        else:
            print('go')
        if usr is not None:
            login(req,usr)
            return redirect(reverse('home'))
    return render(req,'anon/login.html')


def signup(req):
    if req.method=='POST':
        name = req.POST['name']
        email = req.POST['email']
        username = req.POST['username']
        password = req.POST['password']
        susr = Suser.objects.create_user(name=name,email=email,username=username,password=password)
        if susr:
            susr.save()
            return redirect(reverse('login'))
    return render(req,'anon/signup.html')


def home(req):
    if req.user.is_authenticated:
        usr=req.user
        posts = Post.objects.all()
        liked = Post.objects.filter(likes=req.user.id)
        cmnt = Comments.objects.all()
        usr_obj = Suser.objects.get(id=usr.id)

        context = {
                'post': posts,
                'cmnts': cmnt,
                'usr':usr,
                'usr_obj':usr_obj,
        }
        return render(req,'anon/home.html',context)
    else:
        return redirect(reverse('login'))


def like_post(req):
    if req.method == 'POST':
        like_id = req.POST['post_id']
        liked = Post.objects.get(id = like_id)
        liked.likes.add(req.user) 
        return redirect('home')


def unlike_post(req):
    if req.method == 'POST':
        like_id = req.POST['post_id']
        liked = Post.objects.get(id = like_id)
        liked.likes.remove(req.user) 
        return redirect('home')


def save_post(req):
    if req.method == 'POST':
        like_id = req.POST['post_id']
        posts = Post.objects.get(id = like_id)
        posts.saved.add(req.user)
        return redirect('home')


def unsave_post(req):
    if req.method == 'POST':
        like_id = req.POST['post_id']
        posts = Post.objects.get(id = like_id)
        posts.saved.remove(req.user)
        return redirect('home')


def comment(req):
    if req.user.is_authenticated:
        if req.method == 'POST':
            cmnt = req.POST['cmnt']
            post = req.POST['post_id']
            own_usr = Suser.objects.get(id=req.user.id)
            post_usr = Post.objects.get(id=post)
            edit = Comments(owner = own_usr,cmnt=cmnt,post=post_usr)
            if edit:
                edit.save()
            return redirect('home')


def chat(req):
    if req.user.is_authenticated:
        usr = req.user
        context = {
                'usr':usr,
        }
        return render(req,'anon/chat.html',context)
    else:
        return redirect(reverse('login'))


def post_add(req):
    if req.user.is_authenticated:
        usr = req.user
        context = {
                'usr':usr
        }
        if req.method=='POST':
            img = req.POST['image']
            caption = req.POST['caption']
            description = req.POST['description']
            tags = req.POST['tags']
            owner = Suser.objects.get(id=req.user.id)
            posts = Post(owner=owner,pic=img,caption=caption,description=description,tag=tags)
            if posts:
                posts.save()
                return redirect(reverse('home'))
        return render(req,'anon/post_add.html',context)
    else:
        return redirect(reverse('login'))


def profile(req,usrname):
    try:
        use = Suser.objects.get(username=usrname)
    except Suser.DoesNotExist:
        return redirect(reverse('login'))
    if req.user.is_authenticated:
        usr = Suser.objects.get(username=req.user)
        post = Post.objects.filter(owner=use.id)
        posts = Post.objects.filter(owner=use.id,saved=use.id)
        follow = Follow.objects.filter(follower=use.id)
        following = Follow.objects.filter(following=use.id)
    context = {
            'usr': usr,
            'use': use,
            'post': post,
            'posts': posts,
            'follow': follow,
            'following': following,
            }
    return render(req,'anon/profile.html',context) 


def follow(req,usrname):
    if req.user.is_authenticated:
        if req.method == 'POST':
            follower = Suser.objects.get(id=req.user.id)
            following = Suser.objects.get(id=req.POST['user_id'])
            if Follow.objects.filter(follower=follower,following=following):
                return redirect('profile',usrname='usrname')
            else:
                follow_ins = Follow(follower=follower,following=following)
                follow_ins.save()
                return redirect('profile', usrname='usrname')

def unfollow(req,usrname):
    if req.user.is_authenticated:
        if req.method == 'POST':
            follower = Suser.objects.get(id=req.user.id)
            following = Suser.objects.get(id=req.POST['user_id'])
            try:
                unfollow_ins = Follow.objects.get(follower=follower,following=following)
                unfollow_ins.delete()
                return redirect(reverse('profile',usrname=usrname))
            except Follow.DoesNotExist:
                return redirect(reverse('home'))


def reset_password(req):
    if req.method=='POST':
        reset = req.POST['reset']
        passw = Suser.objects.filter(username=reset) | Suser.objects.filter(email=reset)
        if passw:
            pwd = passw[0].password
            m = passw[0].email
            mail = str(m)
            e = mail[:mail.index('@')]
            b = pwd+e
            cryp = crypt(b,'cr')
            c=cryp[2:]
            if c:
                send_mail(
                    'to change password',
                    'http://127.0.0.1:8000/reset/'+c,
                    'yadavmayank848@gmail.com',
                    [passw[0].email],
                    fail_silently=False,
                )
            passw.update(reset_link=cryp)
            return redirect(reverse('login'))
            
        elif Suser.DoesNotExist:
            return redirect(reverse('reset'))
    
    return render(req,'anon/reset_password.html')


def reset_link(req,urn):
    ur = Suser.objects.get(reset_link='cr'+urn)
    passrd = ur.password
    link = ur.reset_link
    em = ur.email
    mail = str(em)
    e = mail[:mail.index('@')]
    if req.method == 'POST':
        if crypt(passrd+em,'cr') == link:
            print('cool')
            password = req.POST['new_password']
            new_password = req.POST['renew_password']
            if password == new_password:
                ur.set_password(password)
                ur.save()
                return redirect(reverse('login'))
        else:
            return redirect(reverse('signup'))
    return render(req,'anon/reset_link.html')

def logut(req):
    logout(req)
    return redirect(reverse('login'))

