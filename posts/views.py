from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from PIL import Image
from .forms import LogInForm, SignUpForm
from django.core.files.images import ImageFile
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import Post, Poster

def signin(request):
    """
        Login page.
    """
    if request.method == 'GET' and 'next' in request.GET:
        next = request.GET['next']
        next = next.replace('/','-')
        print("hello",next)
    else:
        next = ' '

    context = {
        'type': 'Login',
        'logInForm': LogInForm,
        'signUpForm': SignUpForm,
        'next': next,
    }
    return render(request, 'posts/landingPage.html', context)

def failedSignin(request):
    """
        Failed signin page.
    """
    context = {
        'type': 'Login',
        'logInForm': LogInForm,
    }
    return render(request, 'posts/failedSignin.html', context)

def userAuthentication(request, next):
    """
        Authenticate the user.
    """
    user = authenticate(request, username=request.POST['handle'], password=request.POST['password'])
    if user is not None:
        login(request, user)
        if next != ' ':
            next = next.replace('-', '/')
            return redirect(next)
        else:
            return HttpResponseRedirect(reverse('posts:posterView', args=[request.POST['handle']]))
    else:
        return HttpResponseRedirect(reverse('posts:failedSignin'))

def signup(request):
    """
        Sign up page.
    """
    context = {
        'type': 'Sign Up',
        'logInForm': LogInForm,
        'signUpForm': SignUpForm,
        'next': ' ',
    }
    return render(request, 'posts/landingPage.html', context)

def makeUser(request):
    """
        Make a new user.
    """
    user = User.objects.create_user(request.POST['handle'], None, request.POST['password'])
    pfp = request.FILES.get('pfp')
    pfp.name = "%s.%s" % (request.POST['handle'], pfp.content_type.split("/")[-1])
    form = SignUpForm(request.POST, request.FILES)
    if form.is_valid():
        newPoster = Poster(user=user, poster_name=request.POST['username'], poster_handle=request.POST['handle'], poster_pfp=pfp, poster_password=request.POST['password'], liked_posts="")
        newPoster.save()
        login(request, user)
        return HttpResponseRedirect(reverse('posts:posterView', args=[request.POST['handle']]))
    else:
        return HttpResponseRedirect(reverse('posts:signup'))

def allPostView(request):
    """
        View all posts regardless of poster.
    """

    if request.user.username == "":
        user = None
    elif request.user.username == "admin":
        return HttpResponseRedirect(reverse('posts:signin'))
    else:
        user = Poster.objects.get(poster_handle=request.user.username)

    if user == None:
        liked_posts_list = ['']
    else:
        if user.liked_posts.split(',') == ['']:
            liked_posts_list = ['']
        elif len(user.liked_posts.split(',')) == 1:
            liked_posts_list = [int(user.liked_posts)]
        else:
            liked_posts_list = user.liked_posts.split(',')
            for i in range(len(liked_posts_list)):
                liked_posts_list[i] = int(liked_posts_list[i])

    latest_post_list = Post.objects.order_by('-pub_date')
    context = {
        'latest_post_list': latest_post_list,
        'handle': 'all',
        'liked_posts': liked_posts_list,
        'user': user,
    }
    return render(request, 'posts/postView.html', context)

def postView(request, twitterHandle):
    """
        View the posts of a specific poster.
    """

    if request.user.username == "":
        user = None
    elif request.user.username == "admin":
        return HttpResponseRedirect(reverse('posts:signin'))
    else:
        user = Poster.objects.get(poster_handle=request.user.username)

    if user == None:
        liked_posts_list = ['']
    else:
        if user.liked_posts.split(',') == ['']:
            liked_posts_list = ['']
        elif len(user.liked_posts.split(',')) == 1:
            liked_posts_list = [int(user.liked_posts)]
        else:
            liked_posts_list = user.liked_posts.split(',')
            for i in range(len(liked_posts_list)):
                liked_posts_list[i] = int(liked_posts_list[i])

    latest_post_list = Post.objects.order_by('-pub_date').filter(poster__poster_handle=twitterHandle)
    context = {
        'latest_post_list': latest_post_list,
        'handle': twitterHandle,
        'liked_posts': liked_posts_list,
        'view': 'postView',
        'user': user,
    }
    return render(request, 'posts/postView.html', context)

@login_required
def posterView(request, twitterHandle):
    """
        Not yet implemented, but will be the 'home page' of the user that logged in.
    """

    if twitterHandle != request.user.username:
        if twitterHandle == "all":
            return HttpResponseRedirect(reverse('posts:allPostView'))
        else:
            return HttpResponseRedirect(reverse('posts:postView', args=[twitterHandle]))

    if request.user.username == "":
        user = None
    elif request.user.username == "admin":
        return HttpResponseRedirect(reverse('posts:signin'))
    else:
        user = Poster.objects.get(poster_handle=request.user.username)

    if user == None:
        liked_posts_list = ['']
    else:
        if user.liked_posts.split(',') == ['']:
            liked_posts_list = ['']
        elif len(user.liked_posts.split(',')) == 1:
            liked_posts_list = [int(user.liked_posts)]
        else:
            liked_posts_list = user.liked_posts.split(',')
            for i in range(len(liked_posts_list)):
                liked_posts_list[i] = int(liked_posts_list[i])

    latest_post_list = Poster.objects.get(poster_handle=twitterHandle).post_set.order_by('-pub_date')
    context = {
        'latest_post_list': latest_post_list,
        'handle': twitterHandle,
        'view': 'posterView',
        'liked_posts': liked_posts_list,
        'user': user,
    }
    return render(request, 'posts/postView.html', context)

def specificView(request, twitterHandle, post_id):
    """
        More detailed view of a post that will eventually allow user to see replies.
    """

    if request.user.username == "":
        user = None
    elif request.user.username == "admin":
        return HttpResponseRedirect(reverse('posts:signin'))
    else:
        user = Poster.objects.get(poster_handle=request.user.username)

    if user == None:
        liked_posts_list = ['']
    else:
        if user.liked_posts.split(',') == ['']:
            liked_posts_list = ['']
        elif len(user.liked_posts.split(',')) == 1:
            liked_posts_list = [int(user.liked_posts)]
        else:
            liked_posts_list = user.liked_posts.split(',')
            for i in range(len(liked_posts_list)):
                liked_posts_list[i] = int(liked_posts_list[i])

    postsAndReplies = []
    post = Post.objects.get(pk=post_id)
    postsWithPossibleReplies = [post]
    postsWithReplies = []
    checkNext = []
    tempReplies = []
    tempList = []
    counter = 1
    possibleReplies = list(Post.objects.order_by('-pub_date').all())[::-1]
    possibleReplies.remove(post)
    while postsWithPossibleReplies != []:
        print(counter)
        print("Posts with possible replies: ",postsWithPossibleReplies)
        for p in postsWithPossibleReplies:
            print("Possible replies: ",possibleReplies)
            for r in possibleReplies:
                if r.replying_to == p:
                    print("Replying to: ", p)
                    print("Reply: ", r)
                    tempReplies.append(r)
            if tempReplies != []:
                tempList.append([p]+tempReplies)
                postsWithReplies.append([p, counter])
                print("List of replies so far: ",tempReplies)
                checkNext += tempReplies
                tempReplies = []
        print("To be checked: ",checkNext)
        postsWithPossibleReplies = checkNext
        checkNext = []
        counter+=1
    if tempList == []:
        tempList = [post]
    print(tempList)
    previousLength = -1
    currentLength = len(tempList)
    while currentLength != previousLength:
        for item in tempList[1:]:
            if item[0] in tempList[0]:
                index = tempList[0].index(item[0])
                tempList[0] = tempList[0][:index]+item+tempList[0][index+1:]
                tempList.remove(item)
        previousLength = currentLength
        currentLength = len(tempList)
    if type(tempList[0]) == list:
        tempList = tempList[0]
    print(postsWithReplies)
    print(tempList)
    context = {
        'post': post,
        'handle': twitterHandle,
        'liked_posts': liked_posts_list,
        'user': user,
        'posts_and_replies': tempList,
        'posts_with_replies': postsWithReplies,
    }
    return render(request, 'posts/specificView.html', context)

@login_required
def like(request, twitterHandle, post_id, basePost_id, currentPage):
    """
        Currently, pressing 'Reply' 'Retweet' or 'Like' just increments the counter, but will change later.
        This is the page that processes these inputs.
    """
    if request.user.username == "":
        user = None
    elif request.user.username == "admin":
        return HttpResponseRedirect(reverse('posts:signin'))
    else:
        user = Poster.objects.get(poster_handle=request.user.username)
    post = Post.objects.get(pk=post_id)
    check = user.liked_posts.split(',')
    if check == ['']:
        check = [user.liked_posts]
    if str(post_id) in check:
        post.likes -= 1
        if len(check) == 1:
            user.liked_posts = ""
        else:
            check.remove(str(post_id))
            user.liked_posts = ','.join(check)
    else:
        post.likes += 1
        if check == ['']:
            check = [str(post_id)]
        else:
            check.append(str(post_id))
        user.liked_posts = ','.join(check)
    post.save()
    user.save()
    if twitterHandle != "all":
        if currentPage == "specificView":
            return HttpResponseRedirect(reverse('posts:specificView', args=[twitterHandle, basePost_id]))
        else:
            if Poster.objects.get(poster_handle=twitterHandle).user.username == user.user.username:
                return HttpResponseRedirect(reverse('posts:posterView', args=[twitterHandle]))
            else:
                return HttpResponseRedirect(reverse('posts:postView', args=[twitterHandle]))
    else:
        return HttpResponseRedirect(reverse('posts:allPostView'))

@login_required
def retweet(request, post_id, twitterHandle):

    if request.user.username == "":
        user = None
    elif request.user.username == "admin":
        return HttpResponseRedirect(reverse('posts:signin'))
    else:
        user = Poster.objects.get(poster_handle=request.user.username)

    post = Post.objects.get(pk=post_id)
    context = {
        'post': post,
        'handle': twitterHandle,
        'user': user,
    }
    return render(request, 'posts/retweet.html', context)

@login_required
def makeRetweet(request, twitterHandle, post_id):
    post = Post.objects.get(pk=post_id)
    content = post.post_content
    href = '"/posts/'+twitterHandle+'/'+str(post_id)+'/"'
    content = "<p>"+request.POST['postContent']+"</p><a href="+href+"><div style='border: 1px solid black'>"+post.poster.poster_name+" @"+post.poster.poster_handle+" <br />"+content+"</div></a>"
    newPost = Poster.objects.get(poster_handle=request.user.username).post_set.create(post_content=content, pub_date=timezone.now())
    post.retweets += 1
    post.save()
    return HttpResponseRedirect(reverse('posts:posterView', args=[twitterHandle]))

@login_required
def new(request, twitterHandle):
    """
        Page for making a new post.
    """
    context = {
        'handle': request.user.username,
    }
    return render(request, 'posts/new.html', context)

@login_required
def createNewPost(request, twitterHandle):
    """
        Recieves POST data from page that creates new posts and actually makes the post.
    """
    newPost = Poster.objects.get(poster_handle=request.user.username).post_set.create(post_content=request.POST['postContent'], pub_date=timezone.now())
    return HttpResponseRedirect(reverse('posts:posterView', args=[twitterHandle]))

@login_required
def reply(request, twitterHandle, post_id):
    if request.user.username == "":
        user = None
    elif request.user.username == "admin":
        return HttpResponseRedirect(reverse('posts:signin'))
    else:
        user = Poster.objects.get(poster_handle=request.user.username)

    post = Post.objects.get(pk=post_id)
    context = {
        'post': post,
        'handle': twitterHandle,
        'user': user,
    }
    return render(request, 'posts/reply.html', context)

@login_required
def makeReply(request, twitterHandle, post_id):
    post = Post.objects.get(pk=post_id)
    reply = Poster.objects.get(poster_handle=request.user.username).post_set.create(post_content=request.POST['postContent'], replying_to=post, pub_date=timezone.now())
    post.replies += 1
    post.save()
    return HttpResponseRedirect(reverse('posts:posterView', args=[twitterHandle]))

@login_required
def logOut(request):
    """
        Logs user out.
    """
    logout(request)
    return HttpResponseRedirect(reverse('posts:signin'))
