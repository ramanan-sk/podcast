from django.shortcuts import render,redirect
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout

User = get_user_model()

def index(request):
    return render(request,'index.html')

def podchannels(request):
    users = User.objects.filter(streamer=True).exclude(username=request.user.username)
    return render(request,'channels.html',{'users':users})
    
def signup(request):
    if request.method == 'POST':
        streamer = request.POST.getlist('streamer')
        streamer = False if not streamer else True
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        channelname = request.POST['channelname']
        print(streamer)
        if password == cpassword:
            if User.objects.filter(email=email).exists():
                messages.info(request,'Email already used')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request,'Username already exists')
                return redirect('signup')
            else:
                user = User.objects.create(username=username,first_name=firstname,last_name=lastname,email=email,channel_name=channelname,streamer=streamer )
                user.set_password(password)
                user.save()
                return redirect('/login')
        else: 
            messages.info(request,'Password mismatch')
            return redirect('signup')
    else:
        return render(request,'signup.html')

def userlogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('/')
        else : 
            messages.info(request,'Invalid Credentials')
            return redirect('userlogin')
    for x in User.objects.all():
        print(x.username)
    else :
        return render(request,'login.html')

def userlogout(request):
    logout(request)
    return redirect('/')

def podstream(request, room_name):
    return render(request, 'stream.html', {
        'room_name': room_name
    })

def podstudio(request,user_name):
    if(request.user.username == user_name):
        return render(request, 'stream.html', {
        'user_name': user_name
    })
    else:
        return redirect('/')
