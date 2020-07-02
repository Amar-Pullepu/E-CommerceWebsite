var phoneFlag = false;
var emailFlag = false;

var pTypingTimer;                //timer identifier
var pDoneTypingInterval = 1500;  //time in ms, 1.5 second for example
var $input = $('#phone');

//on keyup, start the countdown
$input.on('keyup', function () {
  clearTimeout(pTypingTimer);
  typingTimer = setTimeout(phoneCheck, pDoneTypingInterval);
});

//on keydown, clear the countdown 
$input.on('keydown', function () {
  clearTimeout(pTypingTimer);
});

var eTypingTimer;                //timer identifier
var eDoneTypingInterval = 1500;  //time in ms, 1.5 second for example
var $input = $('#email');

//on keyup, start the countdown
$input.on('keyup', function () {
  clearTimeout(eTypingTimer);
  typingTimer = setTimeout(emailCheck, eDoneTypingInterval);
});

//on keydown, clear the countdown 
$input.on('keydown', function () {
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
        url: '/account/phoneEditCheck',
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
        url: '/account/emailEditCheck',
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
    return true;
}