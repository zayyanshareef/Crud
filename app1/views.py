from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib import messages


# Create your views here.


def signupPage(request):
    
    if 'admin' in request.session:
        return redirect('admin')
    
    if request.session:
        return redirect('home')
  
    elif request.method == 'POST':
        uname = request.POST.get('username')
        if not uname:
            messages.info(request,"Username Can't Be Blank")
            return redirect('signup')
        email = request.POST.get('email')
        if User.objects.filter(email=email).exists():
                messages.info(request, "Email Already Taken")
                return redirect('signup')

        
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        print(uname,"----",email,"----",pass1,"---",pass2,"----")


            
        if pass1 != pass2:
            messages.info(request,"Password Mismatch")
            return redirect('signup')

        else:
            if User.objects.filter(username=uname).exists():
                messages.info(request, "Username Already Taken")
                return redirect('signup')

            else:
                my_user = User.objects.create_user(uname,email,pass1)
                my_user.save()

        return redirect ('login')    
   
    return render(request,'signup.html')       

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def loginPage(request):
    if 'username' in request.session:
        return redirect(homePage)
    elif 'admin' in request.session:
        return redirect('admin')
    else:
        if request.method != 'POST':
            return render (request,'login.html')
        username = request.POST.get('username')
        pass1=request.POST.get('pass')
        User=authenticate(request,username=username,password=pass1)
        print(User,"------")

        if not username :
            messages.info(request,"Username Can't Be blank")
            return redirect('login')
        elif not pass1:
            messages.info(request,"Password Can't be blank")
            return redirect('login')

        if User is not None:
            request.session['username']=username
            login(request,User)
            return redirect('home')

        else:
            return HttpResponse("username or password is incorrect")

@login_required(login_url='login')
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def homePage(request):

    if 'username' not in request.session:
        return redirect('login')
    temp = {"username":request.session['username']}
    context = {'temp':temp}
    return render(request,'home.html',context)
    

@login_required(login_url='login')
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def LogoutPage (request):
    if 'username' in request.session:
        del request.session['username']
    logout(request)
    return redirect('login')

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def adminpage(request):
    # sourcery skip: remove-unnecessary-else, swap-if-else-branches
    
    if 'username' in request.session:
        return redirect('home')
    elif 'admin' in request.session:
        return redirect('dashboard')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            pass1=request.POST.get('pass')
            User=authenticate(request,username=username,password=pass1)
            print(User,"-------------")

            if User is not None and User.is_superuser:
                request.session['admin']=username
                login(request,User)
                return redirect('dashboard')
            
            else:
                return HttpResponse("username or password is incorrect")
            

        
            
    return render (request,'admin_login.html')




@login_required(login_url='admin')
@login_required(login_url='login')
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def dashboard(request):
    if 'admin' in request.session:
        users = User.objects.filter(is_staff= False)
        context = {
            'users' : users,
        }
        return render(request,'crud.html',context)
    
    return redirect('dashboard')


@login_required(login_url='login')
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def admin_logout(request):
    if 'admin' in request.session:
        del request.session['admin']
    logout(request)
    return redirect('admin')

def add(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')


        user = User.objects.create_user(
            username = name,
            email    = email,
            password = password,
        )
        
        return redirect('dashboard')
    
    return render(request,'crud.html')



def edit(request):
    des = des.objects.all()

    context = {
        'des' : des,

    }

    return redirect(request,'crud.html',context)


def update(request, id):
    
    user = User.objects.get(id=id)
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user.username = name
        user.email = email
        if password:
            user.set_password(password)
        user.save()
        return redirect('dashboard')
    else:
        context = {
            'user': user
        }
        return render(request, 'crud.html', context)




def delete(request,id):
    des = User.objects.filter(id=id)
    des.delete()
    
    return redirect('dashboard')




def search(request):
    query = request.GET.get('q')
    if query :
        results = User.objects.filter(username__icontains=query).exclude(username='admin')   
    else:
        results = []
    context = {
        'users': results,
        'query': query,
    }
    return render(request, 'crud.html', context)

