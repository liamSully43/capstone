# Simply Password

## Introduction
Simply Password is a web application that functions as a password manager. It supports capabilities such as; an account system, saving passwords, encrypting & decrypting passwords, updating passwords, deleting passwords and searching for saved passwords. Each password saved is displayed in a list layout.

## Distinctiveness and Complexity

### Distinctiveness - 
Simply Password is quite different from any previous projects due to the other projects not being similar or related to the password manager concept. Although some of the earlier projects either contained or were focused around a search functionality, and this project includes a search functionality, I still believe this project differs from the rest simply because the search feature in Simply Password is more of a secondary or minor feature rather than a leading functionality. The "meat and potatoes" of this project is the ability to save, manage and encrypt passwords in a secure manner, something that the previous projects have not touched on.

### Complexity - 
I believe that this project supplies enough complexity due to the nature of the project; anything involved with security and/or encryption is unlikely to be simple or basic. The code I have written on the backend will handle any kind of CRUD functionality for the user and password models. The code on the frontend is capable of collecting user data to be sent to the backend and will update the frontend with the result of any backend requests, e.g. removing or hiding a password after it has been successfully deleted. The search function is also handled on the front end; it searches both the URL and login for each password and will hide those that don't match the search criteria.

There is also a password authentication feature built-in that will request the user to enter the master password (the password for their Simply Password account) for any functionality that affects saved passwords, such as; viewing, updating and deleting passwords. After successfully entering the master password, the user will not need to enter it again for another 10 minutes. The two exceptions to this are deleting passwords and the first action after logging in. Since deleting a password is quite an important task, the users will need to enter their master password to authenticate the action regardless of how recently they have entered their master password. After logging in, users will need to enter their master password when completing the first action of that session that affects a saved password. Once that authentication has cleared, they will only be prompted again after 10 minutes, with the exception of deleting a password.

## What is Contained in Each File -

### urls.py, admin.py, apps.py, tests.py, style.css & layout.html
None of these files contain anything out of the ordinary. They either remain unchanged from when they were first provided or only have obvious and simple changes that make the application work, e.g. urls.py containing the different URL paths a user can utilise.

### models.py
The models file contains two models, User and WebPassword.

User is the default user model used for user accounts, the only slight variation being the addition of an ID used for the primary key and the __str__ function used to return the username of an account.

The WebPassword model is used for the passwords that a user will save to their account. Included in the WebPassword model is; id for use as a primary key, url to store the URL of the website, username to store the username of the website, password to store the encrypted password of the website, and user_id to store the ID of the associated user. 

### views.py

This file contains all of the functions that are used on the backend.

##### index
This function returns the index page

##### auth_login
This will authenticate a login request and will redirect the user to the passwords page if they are successful, unless the request is a GET request in which case the user will be redirected to either the login page or passwords page depending on if they are logged in or not.

##### auth_register
This will create a new user based on user-inputted data and redirect them to the passwords page, or if it's a GET request they will be redirect to either the register page or passwords page depending on if they are logged in or not.

##### auth_logout
This logs a user out and redirects them to the index page.

##### passwords
This will display the passwords page and fetch all of the user's saved passwords.

##### add_password
Saves a new password

##### encrypt_password
This takes a password, encrypts it and returns the encrypted password.

##### dencrypt_password
See above, but in reverse

##### check_password
This checks if a entered password is the master password of the logged-in user

##### update_password
This will update the details of a saved password

##### delete_password
This deletes a saved password

### app.js
This JavaScript file contains all of the functions used on the frontend.

##### addPasswordBtn.addEventListener
Shows the 'add password' popup when the 'add password' button is clicked

##### addPasswordBg.addEventListener
Hide the 'add password' popup when the grey background is clicked

##### checkPasswordBg.addEventListener
Hide the 'check password' popup when the grey background is clicked

##### checkPasswordExpiry
This checks when the master password was last entered, if the time has expired it will call the showPasswordForm function, if the time hasn't expired it will call the callback method.

##### showPasswordForm
This displays the 'check password' popup to get the user to enter their master password.

##### authenticatePassword
This makes an API request to the backend to see if the inputted password matches the logged in user's master password. If the password is correct it will set the expiration for 10 minutes time and call the passed through callback method. If the password is incorrect it will display an error message stating so

##### prepShowPassword
This function is a 'middle-man' function between the user clicking on the show password button and the checkPasswordExpiry function, it's used to hide the password if the password is already showing or call the checkPasswordExpiry function if it's hidden.

##### showPassword
This shows the selected password for the user to copy

##### prepUpdatePassword
Like the prepShowPassword function, this function acts like a 'middle man' of sorts between the user updating the password and the checkPasswordExpiry function. It prevents the form from actually submitting and the page refreshing when a user updates a password.

##### updatePassword
This makes an API request to the backend to update the selected saved password.

##### prepDeletePassword
This calls the showPasswordForm function to prompt the user to enter the master password before deleting the password. I could have added the call to the showPasswordForm function within the deletePassword function but once the password form is shown, the deletePassword function would continue and delete the password without needing the user to enter their master password. With this prepDeletePassword function, once the showPasswordForm function has finished, there is no more code to be run until the user successfully enters the password - at which point the passed through callback (the deletePassword function) is then called and the password is then deleted. This is a similar process and justification for the previous prep... functions.

##### deletePassword
This deletes the selected saved password

##### searchPasswords
This will search through each password displayed on the page and hide those whose URLs or usernames don't match the search criteria.

### login.html & register.html
These HTML file contain the forms required to either login or register an account.

### passwords.html
This displays all of the user's saved passwords and the search passwords search bar. As well as the add, show, update and delete password buttons

## How to Run Simply Password
Via a terminal, head into the root directory of the project. If you can see two subdirectories called "capstone" and "simply_password" then you're in the right directory, it should be the directory that contains this README.md file. Enter the command "python manage.py runserver" and you should be good!

## Additional Information

### requirements.txt
I didn't want to use any external packages to avoid any conflicts or complications, it also gave me the opportunity to create my own encryption algorithm which I haven't done before but have wanted to do for a while. It's a fairly simple encryption & decryption algorithm, but it works.