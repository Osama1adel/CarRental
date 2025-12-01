from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout

# Create your views here.


def login_view(requset): 
    if requset.method == "POST": 
        email = requset.POST["email"]
        password = requset.POST["password"]

        user = authenticate(requset,username=email,password=password)
        
        if user :
            login(requset,user)
            messages.success(requset,"Logged in successfuly","alert-success")

            return redirect(requset.GET.get("next","/"))
        
        else :
            messages.error(requset,"Email or Passwords dosen't match !","alert-danger")

    return render(requset,"accounts/login.html")




def register_view(requset): 
    if requset.method == "POST" :
        try :
            if requset.POST["password"] != requset.POST["password2"] :
                messages.error(requset,"Passwords dosen't match !","alert-danger")
            
            new_user = User.objects.create_user(username=requset.POST["email"],password=requset.POST["password"],first_name=requset.POST["username"])
            new_user.save()
            # profile = Profile.objects.create(user=new_user)
            messages.success(requset,"Registration Successfuly","alert-success")
            return redirect("accounts:login")

        except Exception as e:
            print(e)
    return render(requset,"accounts/registration.html")




def logout_view(requset):
    logout(requset)
    messages.success(requset,"Logged out Successfuly","alert-success")
    return redirect(requset.GET.get("next","/"))