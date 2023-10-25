"use strict";

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
