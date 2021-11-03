from django.shortcuts import render, redirect
from .models import Room, Topic, Message, User
from .forms import RoomForm, UserForm, MyUserCreationFomr
from django.db.models import Q
#from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm



def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist !')

        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')

        else:
            messages.error(request, 'Username or Password does not exist !')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)



def logoutUser(request):
    logout(request)
    return redirect('login')


def registerUser(request):

    if request.user.is_authenticated:
        return redirect('home')

    form = MyUserCreationFomr()
    if request.method == 'POST':
        form = MyUserCreationFomr(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        
        else:
            messages.error(request, 'An error occured during registration')

    context = {'form': form}
    return render(request, 'base/login_register.html', context)


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q) |
        Q(host__username__icontains=q)
    )

    rooms_count = rooms.count()
    topics = Topic.objects.all()
    room_msgs = Message.objects.filter(room__topic__name__icontains=q)


    context = {
        'rooms': rooms,
        'topics': topics,
        'rooms_count': rooms_count,
        'room_msgs': room_msgs
    }
    return render(request, 'base/home.html', context)


@login_required(login_url='login')
def room(request, pk):
    room = Room.objects.get(id=pk)
    messagess = room.message_set.all().order_by('-created')
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
           user=request.user,
           room=room,
           body=request.POST.get('body') 
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {
        'room':room,
        'messagess': messagess,
        'participants': participants
    }
    return render(request, 'base/room.html', context)


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()

    if request.method == 'POST':
        # topic_name = request.POST.get('topic')
        # topic, created = Topic.objects.get_or_create(name=topic_name)
        
        # room = Room.objects.create(
        #     host=request.user,
        #     topic=topic,
        #     name=request.POST.get('name'),
        #     description=request.POST.get('description')
        # )
        # room.participants.add(request.user)

        # return redirect('home')

        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.save()
            room.participants.add(request.user)
            return redirect('home')

    context = {
        'form': form,
        'topics': topics
    }
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.user != room.host:
        return HttpResponse('Not Allowed !')

    if request.method == 'POST':
        # topic_name = request.POST.get('topic')
        # topic, created = Topic.objects.get_or_create(name=topic_name)

        # room.name = request.POST.get('name')
        # room.topic = topic
        # room.description = request.POST.get('description')

        # return redirect('home')

        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')

    context={'obj': room}
    return render(request, 'base/delete.html', context)



@login_required(login_url='login')
def deleteMessage(request, pk, rpk):
    message = Message.objects.get(id=pk)
    room = Room.objects.get(id=rpk)

    if request.user != message.user:
        return HttpResponse('Not Allowed !')

    if request.method == 'POST':
        message.delete()
        return redirect('room', pk=rpk)

    context={'obj': message}
    return render(request, 'base/delete.html', context)


@login_required(login_url='login')
def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_msgs = user.message_set.all()
    topics = Topic.objects.all()
    context = {
        'user': user,
        'rooms': rooms,
        'room_msgs': room_msgs,
        'topics': topics,
    }
    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST,request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', pk=user.id)
        else:
            print('xx')
    context = {
       'form': form 
    }
    return render(request, 'base/edit-user.html', context)



def topicsPage(request):
    topics = Topic.objects.all()

    context = {'topics': topics}
    return render(request, 'base/topics.html', context)


def activitysPage(request):
    room_msgs = Message.objects.all()[:3]

    context = {'room_msgs': room_msgs}
    return render(request, 'base/activity.html', context)