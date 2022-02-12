const addPasswordBtn = document.querySelector("#add-password-btn");
const addPasswordBg = document.querySelector("#new-password");
const checkPasswordBg = document.querySelector("#check-password");

// show the add new password popup when the add new password button is clicked
addPasswordBtn.addEventListener("click", () => {
    addPasswordBg.classList.remove("hide");
})

// hide the add new password popup when the grey/dark background is clicked
addPasswordBg.addEventListener("click", event => {
    if(event.path[0] == addPasswordBg) { // only hide the pop-up if the background is clicked, if any child elements are clicked do not hide it
        addPasswordBg.classList.add("hide");
        const form = addPasswordBg.children[0].children[1];
        for(let input of form.children) {
            // reset/clear the form inputs, except the hidden CSRF & input button values
            if(["url", "login", "password"].indexOf(input["name"]) > -1) {
                input.value = "";
            }
        }
    }
})

// hide the check password popup when the grey/dark background is clicked
checkPasswordBg.addEventListener("click", event => {
    if(event.path[0] == checkPasswordBg) { // only hide the pop-up if the background is clicked, if any child elements are clicked do not hide it
        checkPasswordBg.classList.add("hide");
        document.querySelector("#password-error").classList.add("hide");
        const form = checkPasswordBg.children[0].children[1];
        const passwordInput = form["password"];
        passwordInput.value = ""; // clear/reset the password input
        // remove the event listener so that it's not actioned when another event listener is added & actioned, and remove the callback
        form.removeEventListener("submit", authenticatePassword)
        form.callback = undefined;
    }
})

// called when viewing, updating or deleting a password. If the password has not be checked/entered in the previous 10 minutes get the user to enter it again.
// the action (e.g. viewing a password) is initially called then checkPasswordExpiry is called to veryify authentication and the action to be completed is passed as a callback
function checkPasswordExpiry(callback) {
    const masterPasswordExpire = localStorage.getItem("masterPasswordTimeStamp") || '0'; // 0 is used if the localStorage has not been set yet
    const expiration = parseInt(masterPasswordExpire);
    const currentTime = new Date().getTime()
    if(expiration < currentTime) {
        showPasswordForm(callback)
    }
    else {
        callback()
    }
}

// this displays the master password checker authenticator and set's up the authenticatePassword eventListener/function
function showPasswordForm(callback) {
    document.querySelector("#check-password").classList.remove("hide");
    const form = document.querySelector("#master-password-form")
    form.addEventListener("submit", authenticatePassword)
    form.callback = callback;
}

function authenticatePassword(event) {
    event.preventDefault() // prevents the form from being submitted and reloading the page
    const callback = event.currentTarget.callback;
    const csrf = event.path[0].csrfmiddlewaretoken.value;
    const password = event.path[0].password.value;

    fetch("/check-password", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrf
        },
        credentials: 'same-origin',
        body: password
    })
    .then(res => res.json())
    .then(data => {
        document.querySelector("#check-password-password").value = ""; // clears the form
        // if succesful, hide the master password pop-up, set a new authenticatio expiration and calls the callback 
        if (data.authenticated) {
            document.querySelector("#password-error").classList.add("hide");
            document.querySelector("#check-password").classList.add("hide");

            const currentTimeStamp = new Date().getTime();
            const newTimeStamp = currentTimeStamp + 600000; // 600000 = 10 minutes in milliseconds
            localStorage.setItem("masterPasswordTimeStamp", newTimeStamp);
            callback()
        }
        // if not succesful, show the error message
        else {
            document.querySelector("#password-error").classList.remove("hide");
        }
    })
}

// this begins the action of showing the password by calling the checkPasswordExpiry function and passing the showPassword action/function as a callback
function prepShowPassword(event) {
    const form = (event.path.length == 8) ? event.path[2]: event.path[1]; // changes depending on which button is clicked
    // if the password is already being displayed, hide it. There's no need to authenticate it
    if(form.password.type === "text") {
        form.password.type = "password";
        return
    }
    checkPasswordExpiry(() => showPassword(event))
}

// shows the selected  password
function showPassword(event) {
    const form = (event.path.length == 8) ? event.path[2]: event.path[1];
    form.password.type = "text";
}

// this begins the action of updating the password by calling the checkPasswordExpiry function and passing the updatePassword action/function as a callback
function prepUpdatePassword(event) {
    event.preventDefault() // prevents the form from being submitted and refreshing the page
    checkPasswordExpiry(() => updatePassword(event))
}

// updates the password with the details stored in the input boxes
function updatePassword(event) {
    const form = event.path[0];
    const url = form.url.value;
    const login = form.login.value;
    const password = form.password.value;
    const passwordId = form.id;
    const csrf = form.csrfmiddlewaretoken.value;
    const data = {
        url,
        login,
        password,
        passwordId
    }

    fetch("/update-password", {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrf
        },
        credentials: 'same-origin',
        body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(data => {
        // if successful add the updated class to the form which highlights the password in green, after 2.5s remove the class.
        if(data.updated) {
            form.classList.add("updated")
            setTimeout(() => {
                form.classList.remove("updated")
            }, 2500)
        }
        else {
            alert("Something went wrong, please try again later") ? "": window.location.reload(); // alert the user something went wrong, then refresh the page to clear any changes made
        }
    })
}

// this begins the action of deleting the password by calling the checkPasswordExpiry function and passing the deletePassword action/function as a callback
function prepDeletePassword(id) {
    showPasswordForm(() => deletePassword(id))
}

// this deletes the selected password
function deletePassword(id) {
    const csrf = document.cookie.split("=")[1]; // gets the csrf token from the cookies
    fetch(`/delete-password/${id}`, {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrf
        },
        credentials: 'same-origin'
    })
    .then(res => res.json())
    .then(data => {
        // if succesful, a deleted-password class is added to the password and then the element is removed
        if(data.deleted) {
            const password = document.getElementById(id);
            password.classList.add("deleted-password");
            setTimeout(() => {
                password.remove()
            }, 1000);
        }
        // if unsuccesful the user is alerted
        else {
            alert("Something went wrong, please try again later");
        }
    })
}

// this searches the passwords using the onKeyUp HTML event
function searchPasswords(searchbar) {
    const searchValue = searchbar.value.toLowerCase();
    const passwords = document.querySelectorAll(".passwords");
    // if the search bar is empty, remove the hide class from all passwords to display all passwords
    if(searchValue === "") {
        for(let password of passwords) {
            password.classList.remove("hide")
        }
        return
    }
    // loop through each password and if neither the URL or login contains the searh criteria, hide the password
    for(let password of passwords) {
        const url = password.url.value.toLowerCase();
        const login = password.login.value.toLowerCase();
        if(url.search(searchValue) < 0 && login.search(searchValue) < 0) {
            password.classList.add("hide")
        }
    }
}