from django.http import HttpResponseNotFound
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
import re
# models & forms
from .models import Post, User, Comment
from .forms import PostForm
# markdownx
from markdownx.utils import markdownify


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    posts = Post.objects.filter(Q(title__icontains=q) | Q(category__icontains=q) | Q(gist__icontains=q))

    context = {'posts': posts}
    return render(request, 'base/home.html', context)


# User auth related
def registerUser(request):
    page = 'register'   

    if request.method == "POST":
        username = request.POST.get('username').lower()
        email = request.POST.get('email')
        password = request.POST.get('password')

        if len(password) >= 8:
            newUser = User.objects.create_user(username, email, password)
            newUser.save()
            login(request, newUser)
            return redirect('home')
        else:
            messages.warning(request, "Password should contain at least 8 characters.")

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def loginUser(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        id = request.POST.get('id').lower()
        password = request.POST.get('password')
        regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        user = None
        if re.fullmatch(regex, id):
            try:
                user = User.objects.get(email=id)
            except:
                messages.error(request, f"User @{id} does not exist.")
            user = authenticate(request, username=user.username, password=password)
        else:
            try:
                user = User.objects.get(username=id)
            except:
                messages.error(request, f"User @{id} does not exist.")
            user = authenticate(request, username=id, password=password)
    
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "UserID OR Password does not match. Please try again.")

    context = {'page':page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def signoutUser(request):
    user = request.user
    user.delete()
    logout(request)
    return redirect('home')

# Profile page
@login_required(login_url='login')
def updateProfile(request, pk):
    user = User.objects.get(id=pk)

    if request.method == "POST":
        username = request.POST.get('username').lower()
        email = request.POST.get('email')
        password = request.POST.get('password')
        if username:
            user.username = username 
        if email:
            user.email = email
        if password:
            user.set_password(password)
        user.save()
        return redirect('home')

    context = {'user':user}
    return render(request, 'base/profile.html', context)

# About page
def about(request):
    return render(request, 'base/about.html')


# blog post (create comment)
def getPost(request, pk):
    post = Post.objects.get(id=pk)
    html = markdownify(post.contents)
    comments = Comment.objects.filter(Q(post_id=post.id))

    if request.method == "POST":
        newComment = request.POST.get('new-comment')
        if newComment:
            if request.user.is_anonymous:
                messages.error(request, "Please login/signup to view/post a comment.")
            else:
                comment = Comment.objects.create(user_id=request.user, post_id=post, contents=newComment)
                comment.save()
                return redirect('post', pk=post.id)
        else:
            messages.error(request, "Can't post a empty comment.")

    context = {'post':post, 'contents':html, 'comments': comments}
    return render(request, 'base/post.html', context)

def createPost(request):
    form = PostForm(request.POST or None)
    context = {'form':form}
    if request.method == "POST":
        if form.is_valid():
            post = form.save(commit=False)
            post.save()        
            return redirect("home") 

    return render(request, 'base/post-form.html', context)


def updatePost(request, pk):
    post = Post.objects.get(id=pk)
    contents = post.contents

    if request.method == "POST":
        title = request.POST.get('title')
        category = request.POST.get('category')
        gist = request.POST.get('gist')
        status = request.POST.get('status')
        contents = request.POST.get('contents')
        if title:
            post.title = title
        if category:
            post.category = category
        if gist:
            post.gist = gist
        if status:
            post.status = status
        post.contents = contents
        post.save()
        return redirect('post', pk=post.id)

    context = {'post':post, 'contents': contents}
    return render(request, 'base/post-update.html', context)
