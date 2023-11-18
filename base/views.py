from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Room,Topic,Message,User
from .forms import RoomForm,UserForm,MyUserCreationForm


# Create your views here.

# rooms = [
#     {'id':1 , "name" : "Lets learn python!"},
#     {'id':2 , "name" : "Design with me"},
#     {'id':3 , "name" : "Frontend Developer"},
# ]

def login_page(request):
    page = 'login'
    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(email = email)
        except:
            messages.error(request,'User dose not exist')
        user = authenticate(request ,email=email,password=password)
        if user is not None:
            login(request , user)
            return redirect('home')
        else:
            messages.error(request,'Username Or Password dose not exist')
        
    context = {'page':page}
    return render(request,'base/login_register.html',context)

def register_page(request):
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'An Erro occuerred during registeration !!')

    return render(request,'base/login_register.html',{'form':form})

def logout_user(request):
    logout(request)
    return redirect('home')


def home(request):
    q = request.GET.get('q') if request.GET.get('q')!= None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains = q) |
        Q(name__icontains=q) |
        Q(descriptions__icontains=q)
        )
    room_count = rooms.count()
    topics = Topic.objects.all()[:4]
    room_messages = Message.objects.filter(Q(room__topic__name__icontains = q))
    context = {'rooms':rooms,'topics':topics,'room_count':room_count,'room_messages':room_messages}
    return render(request,'base/home.html',context)

def room(request,pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    if request.method == 'POST':
        add_conversation = Message.objects.create(
        user = request.user,
        room = room,
        body = request.POST.get('body'),
    ) 
        room.participants.add(request.user)
        return redirect('room' , pk=room.id)
    
    
    context = {'room':room , 'room_messages':room_messages , 'participants':participants}
    
    return render(request,'base/room.html',context)

def user_profile(request,pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context={'user':user,'rooms':rooms,'room_messages':room_messages,'topics':topics}
    return render(request,'base/profile.html',context)


@login_required(login_url='login')
def create_room(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            descriptions=request.POST.get('descriptions'),
        )
        return redirect('home')

    context = {'room_form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def update_room(request,pk):
    room = Room.objects.get(id = pk)
    form = RoomForm(instance = room)
    topics = Topic.objects.all()
    if request.method == 'POST':
        # form = RoomForm(request.POST,instance = room)
        # if form.is_valid():
        #     form.save()
        #     return redirect('home')
        topic_name = request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name=topic_name)
        room.host = request.user
        room.name = request.POST.get('name')
        room.topic = topic
        room.descriptions = request.POST.get('descriptions')
        room.save()
        return redirect('home')
    
    context = {"room_form" : form,'topics':topics,'room':room}
    return render(request,'base/room_form.html',context)

@login_required(login_url='login')
def delete_room(request,pk):
    data = Room.objects.get(id = pk)
    if request.method == 'POST':
        data.delete()
        return redirect('home')
    
    context = {'name':data.name}
    return render(request,'base/delete.html',context)

@login_required(login_url='login')
def delete_message(request,pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse("You are Not allowed Her !!")
    
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'name' :message})

@login_required(login_url='login')
def update_user(request,pk):
    user = User.objects.get(id=pk)
    form = UserForm(instance = request.user)
    if request.method == 'POST':
        form = UserForm(request.POST,request.FILES,instance=user)
        
        if form.is_valid():
            form.save()
            return redirect('profile',pk = user.id)
        
    return render(request,'base/update-user.html' , {'form':form})


def topic_page(request):
    q = request.GET.get('q') if request.GET.get('q') !=None else ''
    topics = Topic.objects.filter(name__icontains = q)
    return render(request,'base/topics.html',{'topics':topics})

def activities_page(request):
    room_messages = Message.objects.all()
    return render(request,'base/activity.html',{'room_messages':room_messages})