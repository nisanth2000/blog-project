from django.shortcuts import render,redirect,get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import BlogPostSerializer
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required
def home(request):
    posts=BlogPost.objects.all()
    return render(request, 'home.html',{'posts': posts})
  

@api_view(['GET'])
def blog_list(request):
    posts = BlogPost.objects.all()
    serializer = BlogPostSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def blog_detail(request, id):
    try:
        post = BlogPost.objects.get(id=id)
    except BlogPost.DoesNotExist:
        return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = BlogPostSerializer(post)
    return Response(serializer.data)

@api_view(['POST'])
def blog_create(request):
    serializer = BlogPostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def blog_update(request, id):
    try:
        # Retrieve the blog post by id
        post = BlogPost.objects.get(id=id)
    except BlogPost.DoesNotExist:
        return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = BlogPostSerializer(post, data=request.data)
    if serializer.is_valid():
        # Save the updated blog post
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def blog_delete(request, id):
    try:
        post = BlogPost.objects.get(id=id)
    except BlogPost.DoesNotExist:
        return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

    post.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})

def post_update(request, id):
    post = get_object_or_404(BlogPost, id=id)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PostForm(instance=post)
    return render(request, 'edit_post.html', {'form': form})

def post_delete(request, id):
    post = get_object_or_404(BlogPost, id=id)
    if request.method == "POST":
        post.delete()
        return redirect('home')
    return render(request, 'delete_post.html', {'post': post})

def login_page(request):
    if request.method == "POST":
        
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user_obj = User.objects.filter(username=username)
            if not user_obj.exists():
                messages.error(request, "Username not found")
                return redirect('/')
            user_obj = authenticate(username=username, password = password)
            if user_obj:
                login(request, user_obj)
                return redirect('/blog/')
            messages.error(request, "Wrong Password")
            return redirect('/')
            
        except Exception as e:
            messages.error(request, " Somthing went wrong")
            return redirect('/register/')
        
    return render(request, "login.html")


def register_page(request):
    if request.method == "POST": 
        try: 
            username = request.POST.get('username')
            password = request.POST.get('password')
            user_obj = User.objects.filter(username=username)
            if user_obj.exists():
                messages.error(request, "Username is taken")
                return redirect('/register/')
            user_obj = User.objects.create(username=username)
            user_obj.set_password(password)
            user_obj.save()
            messages.success(request, "Account created")
            return redirect('/')

        except Exception as e:
            messages.error(request, " Somthing went wrong")
            return redirect('/register/')
        
    return render(request, "register.html")
def logout_view(request):
    logout(request)  
    return redirect('/')  


