from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from .models import User, WebPassword
import json

# Create your views here.

def index(request):
    return render(request, "pages/index.html")

def auth_login(request):
    if request.method == "POST":
        # collect user input
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        # if the user exists, log them in
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("passwords"))
        else:
            return render(request, "pages/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        # if /login is visited via GET
        if request.user.is_authenticated:
            return HttpResponseRedirect("passwords")
        else:
            return render(request, "pages/login.html")

def auth_register(request):
    if request.method == "POST":
        # collect user input
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm"]

        if password != confirm_password:
            return render(request, "pages/register.html", {
                "message": "Passwords must match."
            })
        # create the user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()

        except IntegrityError:
            return render(request, "pages/register.html", {
                "message": "Username already taken."
            })
        # log the user in after creating their account
        login(request, user)
        return HttpResponseRedirect(reverse("passwords"))
    else:
        # if /register is visited via GET
        if request.user.is_authenticated:
            return HttpResponseRedirect("passwords")
        else:
            return render(request, "pages/register.html")

def auth_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def passwords(request):
    if request.user.is_authenticated:
        # get all of the user's passwords
        try:
            password_list = WebPassword.objects.filter(user_id=int(request.user.id))
            for password in password_list:
                # decrypt the password
                decrypted_password = decrypt_password(password.password)
                password.password = decrypted_password
            all_passwords = password_list
            message = False
        except:
            message = "Unable to load passwords, please try again later."
            all_passwords = []
        
        return render(request, "pages/passwords.html", {
            "user": request.user,
            "passwords": all_passwords,
            "message": message,
            "length": len(all_passwords)
        })
    else:
        return HttpResponseRedirect(reverse("login"))

def add_password(request):
    if request.method == "POST":
        # collect user input
        url = request.POST["url"]
        username = request.POST["login"]
        password = request.POST["password"]
        user__id = request.user.id
        # encryt the password
        encrypted_password = encrypt_password(password)
        # save the password
        new_password = WebPassword(
            url=url,
            username=username,
            password=encrypted_password,
            user_id=user__id
        )
        new_password.save()
    
    return HttpResponseRedirect(reverse("passwords"))

# custom encryption function
def encrypt_password(password):
    alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    alphabetCap = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    encrypted_password = ""
    for char in password:
        if char.isalpha(): # check if the character is a letter
            if char.isupper(): # check if the character is upper case
                index = alphabetCap.index(char) # find the index of the letter in the alphabet
                # add one onto the index so that letter becomes the next letter in the alphabet after encryption
                index += 1 
                if index >= 26: # if the letter is 'z' it will need to restart at 'a'
                    index = 0
                encrypted_password += alphabetCap[index]
            else:
                # same as above but for lower case characters
                index = alphabet.index(char)
                index += 1
                if index >= 26:
                    index = 0
                encrypted_password += alphabet[index]
        elif char.isdigit(): # check if the character is a digit
            num = int(char)
            # add one onto the number, since it's encrypted on a character by character basis - 9 will need to be encypted into 0
            num += 1
            if num == 10:
                num = 0
            str_num = str(num)
            encrypted_password += str_num
        else: # if the character is not a number or letter then just add the character to the encrypted password
            encrypted_password += char
    
    return encrypted_password

# password are decrypted but reversing the process of the above function
def decrypt_password(password):
    alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    alphabetCap = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    decrypted_password = ""
    for char in password:
        if char.isalpha(): # check if letter
            if char.isupper(): # check if uppercase
                index = alphabetCap.index(char)
                # remove one from the index to get the original letter, if the index is less than  zero then it needs to be set to 25
                index -= 1
                if index <= -1:
                    index = 25
                decrypted_password += alphabetCap[index]
            else:
                # same as above but for lower case characters
                index = alphabet.index(char)
                index -= 1
                if index <= -1:
                    index = 25
                decrypted_password += alphabet[index]
        elif char.isdigit(): # check if character is a digit
            num = int(char)
            # remove one from the number to get the original number
            # if the number is less than zero then it means the number was originally nine
            num -= 1
            if num < 0:
                num = 9
            str_num = str(num)
            decrypted_password += str_num
        else:
            decrypted_password += char
    
    return decrypted_password

# user for checking the master password when viewing, updating or deleting passwords
def check_password(request):
    password = request.body.decode("utf-8")
    username = request.user.username
    user = authenticate(request, username=username, password=password)
    if user != None and user.id == request.user.id:
        # correct password entered
        return JsonResponse({"authenticated": True})
    else:
        # incorrect password entered
        return JsonResponse({"authenticated": False})

# update the password with the provided details
def update_password(request):
    # collect the user input
    body = request.body.decode("utf-8")
    data = json.loads(body)
    url = data["url"]
    username = data["login"]
    password = data["password"]
    password_id = int(data["passwordId"])
    # update the password
    try:
        saved_password = WebPassword.objects.get(pk=password_id)

        # if the password or password ID doesn't exist, send back the False value
        if saved_password.user_id != request.user.id:
            return JsonResponse({"updated": False})

        # encrypt the password
        encrypted_password = encrypt_password(password)

        saved_password.url = url
        saved_password.username = username
        saved_password.password = encrypted_password

        # update/save the password
        saved_password.save()
        return JsonResponse({"updated": True})
    except:
        # any errors or issues, send back the False value
        return JsonResponse({"updated": False})

# deletes passwords
def delete_password(request, password_id):
    # try to delete the password, send back True or False depending on if succesful or not, respectively
    try:
        password = WebPassword.objects.get(pk=int(password_id))
        password.delete()
        return JsonResponse({"deleted": True})
    except:
        return JsonResponse({"deleted": False})
