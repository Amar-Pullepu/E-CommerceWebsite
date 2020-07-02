var phoneFlag = false;
var emailFlag = false;
var passwdFlag = false;
var rePasswdFlag = false;

var $passwd = $('#password');
$passwd.on('input', function () {
    checkPassword()
});

var $repasswd = $('#repassword');
$repasswd.on('input', function () {
    checkRePassword()
});

var pTypingTimer;                //timer identifier
var pDoneTypingInterval = 1500;  //time in ms, 3 second for example
var $pinput = $('#phone');

//on keyup, start the countdown
$pinput.on('keyup', function () {
  clearTimeout(pTypingTimer);
  typingTimer = setTimeout(phoneCheck, pDoneTypingInterval);
});

//on keydown, clear the countdown 
$pinput.on('keydown', function () {
  clearTimeout(pTypingTimer);
});

var eTypingTimer;                //timer identifier
var eDoneTypingInterval = 1500;  //time in ms, 3 second for example
var $einput = $('#email');

//on keyup, start the countdown
$einput.on('keyup', function () {
  clearTimeout(eTypingTimer);
  typingTimer = setTimeout(emailCheck, eDoneTypingInterval);
});

//on keydown, clear the countdown 
$einput.on('keydown', function () {
  clearTimeout(eTypingTimer);
});

function phoneCheck() {
    phoneFlag = true;
    var phone = document.getElementById("phone").value;
    var patt = new RegExp("[0-9]{10}");
    if(phone.length !== 10 || !patt.test(phone)){
        document.getElementById("phone").style.borderColor  = "#e03024";
        phoneFlag = false;
        return;
    }
    $.ajax({
        url: '/account/phoneCheck',
        async: false,
        data: {
          'Phone': phone
        },
        dataType: 'json',
        success: function (data) {
          if (data.Exist == "True") {
            phoneFlag = false;
          }
        }
      });
    
    if(!phoneFlag){
        document.getElementById("phone").style.borderColor  = "#e03024";
    }
    else{
        document.getElementById("phone").style.borderColor = "#34eb4f";
    }
}

function emailCheck() {
    var email = document.getElementById("email").value;
    emailFlag = true;
    if (!(/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(email)))
    {
        document.getElementById("email").style.borderColor  = "#e03024";
        emailFlag = false;
        return
    }
    $.ajax({
        url: '/account/emailCheck',
        async: false,
        data: {
          'Email': email
        },
        dataType: 'json',
        success: function (data) {
          if (data.Exist == "True") {
            emailFlag = false;
          }
        }
      });
    if(!emailFlag){
        document.getElementById("email").style.borderColor  = "#e03024";
    }
    else{
        document.getElementById("email").style.borderColor = "#34eb4f";
    }
}

function checkPassword() {
    var passwd = document.getElementById("password").value;
    passwdFlag = false;
    if(passwd.length < 8){
        document.getElementById("password").style.borderColor  = "#e03024";
    }
    else{
        document.getElementById("password").style.borderColor = "#34eb4f";
        passwdFlag = true;
    } 
}

function checkRePassword() {
    var rePasswd = document.getElementById("repassword").value;
    var passwd = document.getElementById("password").value;
    rePasswdFlag = false;
    if(rePasswd !== passwd){
        document.getElementById("repassword").style.borderColor  = "#e03024";
    }
    else{
        document.getElementById("repassword").style.borderColor = "#34eb4f";
        rePasswdFlag = true;
    } 
}

function beforeSubmit() {
    phoneCheck()
    emailCheck()
    checkPassword()
    checkRePassword()
    if(!emailFlag){
        alert("Email address already exists!");
        return false;
    }
    if(!phoneFlag){
        alert("Phone number already exists!");
        return false;
    }
    if(!passwdFlag){
        alert("Password length should be minimum 8 Charecters");
        return false;
    }
    if(!rePasswdFlag){
        alert("Both passwords didn't match");
        return false;
    }
    return true;
}