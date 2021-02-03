from operator import or_
from functools import reduce
import re

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.db.models import Q
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import EditUserForm, EditProfileForm
from .models import MessageBoardCategory, MessageBoardPost, Profile, Message

def index(request):
    posts = []
    for i in MessageBoardPost.objects.order_by('-date_posted')[:3:]:
        post = {}
        post["poster"] = i.poster
        post["tstamp"] = i.date_posted.strftime("%b %d, %I:%M %p")
        post["message_title"] = i.message_title
        post["message_body"] = i.message_body
        post["id"] = i.id
        posts.append(post)
    args = {'user': request.user, 'posts': posts} #.filter(category=MessageBoardCategory.objects.get(id=2)
    return render(request, 'studentmatching/index.html', args)

@login_required(login_url='/')
def help(request):
    return render(request, 'studentmatching/help.html')

@login_required(login_url='/')
def logout(request):
    auth_logout(request)
    return redirect('/')

@login_required(login_url='/')
def view_profile(request):
    args = {'user': request.user}
    return render(request, 'studentmatching/view_profile.html', args)

@login_required(login_url='/')
def submit_profile(request):
    prepopulate_1 = {
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'email': request.user.email,
    }
    prepopulate_2 = {
        'major': request.user.profile.major,
        'minor': request.user.profile.minor,
        'classes_taken': request.user.profile.classes_taken
    }
    if request.method == 'POST':
        user_form = EditUserForm(request.POST, instance=request.user, initial=prepopulate_1)
        profile_form = EditProfileForm(request.POST, instance=request.user.profile, initial=prepopulate_2)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            args = {'user': request.user}
            return render(request, 'studentmatching/view_profile.html', args)
    else:
        user_form = EditUserForm(instance=request.user, initial=prepopulate_1)
        profile_form = EditProfileForm(instance=request.user.profile, initial=prepopulate_2)
        args = {'user_form': user_form, 'profile_form': profile_form, 'user': request.user, 'error':True, 'error_message': "An error has occured!"}
        return render(request, 'studentmatching/edit_profile.html', args)

@login_required(login_url='/')
def edit_profile(request):
    prepopulate_1 = {
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'email': request.user.email,
    }
    prepopulate_2 = {
        'major': request.user.profile.major,
        'minor': request.user.profile.minor,
        'classes_taken': request.user.profile.classes_taken
    }
    if request.method == 'POST':
        user_form = EditUserForm(request.POST, instance=request.user, initial=prepopulate_1)
        profile_form = EditProfileForm(request.POST, instance=request.user.profile, initial=prepopulate_2)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('/')
    else:
        user_form = EditUserForm(instance=request.user, initial=prepopulate_1)
        profile_form = EditProfileForm(instance=request.user.profile, initial=prepopulate_2)
        args = {'user_form': user_form, 'profile_form': profile_form, 'user': request.user}
        return render(request, 'studentmatching/edit_profile.html', args)

@login_required(login_url='/')
def get_profile(request, username):
    user = User.objects.get(username=username)
    args = {'user': user}
    return render(request, 'studentmatching/profile.html', args)

@login_required(login_url='/')
def view_post(request, post_id):
    post = MessageBoardPost.objects.get(id=post_id)
    return render(request, 'studentmatching/messageboardpost_detail.html', {'post': post})

class MessageBoardCategoryIndex(LoginRequiredMixin, generic.ListView):
    login_url = '/'
    redirect_field_name = 'redirect_to'
    model = MessageBoardCategory
    template_name = 'studentmatching/messageboardcategory_index.html'
    context_object_name = 'message_board_category_list'

    def get_queryset(self):
        return MessageBoardCategory.objects.all()

class MessageBoardPostIndex(LoginRequiredMixin, generic.DetailView):
    login_url = '/'
    redirect_field_name = 'redirect_to'
    model = MessageBoardCategory
    template_name = 'studentmatching/messageboardpost_index.html'
    context_object_name = 'messageboardcategory'

class MessageBoardPostCreate(LoginRequiredMixin, generic.ListView):
    login_url = '/'
    redirect_field_name = 'redirect_to'
    model = MessageBoardCategory
    template_name = 'studentmatching/messageboardpost_create.html'
    context_object_name = 'message_board_category_list'

class MessageBoardPostDetail(LoginRequiredMixin, generic.DetailView):
    login_url = '/'
    redirect_field_name = 'redirect_to'
    model = MessageBoardPost
    template_name = 'studentmatching/messageboardpost_detail.html'

@login_required(login_url='/')
def make_post(request):
    messageboardpost = MessageBoardPost()
    messageboardpost.message_title = request.POST.get('message_title', "default")
    messageboardpost.message_body = request.POST.get('message_body', "default")
    messageboardpost.poster = User.objects.get(pk = request.POST.get('poster'))
    """
    try:
        messageboardpost.poster = request.POST.get('poster')
    except (KeyError, User.DoesNotExist):
        return render(request, 'studentmatching/index.html', {
            'error_message': "User could not be found. Are you logged in?"
        })
    """
    try:
        messageboardpost.category = MessageBoardCategory.objects.get(id=request.POST.get('messageboardcategory'))
    except (KeyError, MessageBoardCategory.DoesNotExist):
        return render(request, 'studentmatching/messageboardcategory_index.html', {
            'error_message': "The category you tried to post under could not be found.",
        })
    messageboardpost.save()
    return HttpResponseRedirect("/post/"+ str(messageboardpost.id) + "/")

@login_required(login_url='/')
def user_search_by_keyword(request):
    if request.method == 'GET':
        words = request.GET.get('search')
        users = []
        profiles = []
        if words is not None:
            words = words.strip()
            keywords = re.split(r',\s|\s', words) #splits the search string into keywords (comma and space delimited)
            q_list_user = []
            q_list_profile = []
            for key in keywords: #creates a query set for the fields that are being searched for each keyword
                q_list_user.append(Q(first_name__icontains=key))
                q_list_user.append(Q(last_name__icontains=key))
                q_list_user.append(Q(username__icontains=key))
                q_list_profile.append(Q(major__icontains=key))
                q_list_profile.append(Q(minor__icontains=key))
                q_list_profile.append(Q(classes_taken__icontains=key))
            users = list(User.objects.filter(reduce(or_, q_list_user))) #looks up the users who match the search criteria
            profiles = list(Profile.objects.filter(reduce(or_, q_list_profile))) #looks up the profile that match the search criteria
        else:
            users = list(User.objects.all()) #looks up the users who match the search criteria
            profiles = list(Profile.objects.all()) #looks up the profile that match the search criteria
        users_1 = map(lambda x: x.user, profiles) #retrieves the corresponding user from their profile
        users.extend(x for x in users_1 if x not in users) #combines the two lists of users, avoiding duplicates
        users = [i for i in users if not i.profile.private] # and i.username != request.user.username
        for i in users:
            i.is_me = i.username == request.user.username
        return render(request, 'studentmatching/search.html', {"users": users, "searched": "" if words is None else words})
        """
        if words is not None:
        else:
            return render(request, 'studentmatching/search.html')
        """
    else:
        return render(request, 'studentmatching/search.html')

@login_required(login_url='/')
def board_search_by_keyword(request):
    if(request.method == 'GET'):
        words = request.GET.get('search')
        posts = []
        if words is not None:
            words.strip()
            keywords = re.split(r',\s|\s', words)
            q_list_post = []
            for key in keywords:
                q_list_post.append(Q(message_title__icontains=key))
                q_list_post.append(Q(message_body__icontains=key))
            posts = list(MessageBoardPost.objects.order_by('-date_posted').filter(reduce(or_, q_list_post)))
            cat_posts = [i for i in MessageBoardPost.objects.order_by('-date_posted') if words in str(i.category)]
            posts.extend(x for x in cat_posts if x not in posts)
            posts.sort(key=lambda x: x.date_posted.timestamp())
            posts = posts[::-1]
        else:
            posts = MessageBoardPost.objects.order_by('-date_posted')
        return render(request, 'studentmatching/board_search.html', {"posts": posts, "searched": "" if words is None else words})
    else:
        return render(request, 'studentmatching/board_search.html')

@login_required(login_url='/')
def view_messages(request):
    received_messages = Message.objects.filter(Q(receiver=request.user) & Q(viewer=request.user)).order_by('date')
    sent_messages = Message.objects.filter(Q(sender=request.user) & Q(viewer=request.user)).order_by('date')
    args = {"received": list(received_messages)[::-1], "sent": list(sent_messages)[::-1]}
    return render(request, 'studentmatching/direct_messages.html', args)

@login_required(login_url='/')
def send_message(request, username):
    send_user = User.objects.filter(username=username)[0]
    if request.method == 'POST':
        content = request.POST.get('content')
        if request.user == send_user:
            Message.objects.create(sender=request.user, receiver=send_user, viewer=request.user, content=content)
            #to avoid duplicates
        else:
            Message.objects.create(sender=request.user, receiver=send_user, viewer=request.user, content=content)
            Message.objects.create(sender=request.user, receiver=send_user, viewer=send_user, content=content)
            #creates two objects so deleting a message does not delete it for the both the sender and receiver
        return redirect('/messages/')
    else:
        return render(request, 'studentmatching/send_message.html', {"user": send_user})

@login_required(login_url='/')
def delete_message(request, pk):
    try:
        message = Message.objects.get(pk=pk)
        #so only the sender or receiver of the message can delete it
        if message.viewer == request.user and (message.sender == request.user or message.receiver == request.user):
            Message.objects.get(pk=pk).delete()
    except Message.DoesNotExist:
        return redirect('/messages/')
    return redirect('/messages/')
