'use strict'


const container = document.querySelector(".container"),
  pwShowHide = document.querySelectorAll(".showHidePw"),
  pwFields = document.querySelectorAll(".password");

//   js code to show/hide password and change icon
pwShowHide.forEach((eyeIcon, index) => {
  eyeIcon.addEventListener("click", () => {
    if (pwFields[index].type === "password") {
      pwFields[index].type = "text";
      eyeIcon.classList.replace("uil-eye-slash", "uil-eye");
    } else {
      pwFields[index].type = "password";
      eyeIcon.classList.replace("uil-eye", "uil-eye-slash");
    }
  });
});


$(document).ready(function(){

    let menues= $("#profile .content-title")

    
    menues.on("click",function(e){
        e.preventDefault();
        $(".active-title").removeClass("active-title")
        $(this).addClass("active-title")
        let id=$(this).data("id")
        $('.item').addClass("d-none");
        $(`.item[data-id=${id}]`).removeClass("d-none")

    })
});