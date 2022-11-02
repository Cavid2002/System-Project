const passwordEye = (password, icon) => {
  if (password.type === "password") {
    password.type = "text";
    icon.innerText = "visibility_off";
  } else {
    password.type = "password";
    icon.innerText = "visibility";
  }
};

const toggleVisibility = () => {
  let password = document.getElementById("password");
  let icon = document.getElementById("icon");
  passwordEye(password, icon);
};

const toggleVisibilityRe = () => {
  let password = document.getElementById("repassword");
  let icon = document.getElementById("iconre");
  passwordEye(password, icon);
};

const toggleVisibilityLog = () => {
    let password = document.getElementById('passwordLog');
    let icon = document.getElementById('iconLog');
    passwordEye(password,icon)
}

// const btn = document.getElementById("signupBtn");
// btn.addEventListener("click", (e) => {
//   // e.preventDefault();

//   // Email validation
//   const emailRegex =
//     /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
//   const email = document.getElementById("email").value;
//   if (email != "") {
//     if (!email.match(emailRegex)) {
//       alert("Email is not correct format");
//     }
//   }

//   // Password equality
//   const password = document.getElementById("password");
//   const repassword = document.getElementById("repassword");
//   if (!(password.value == "" || repassword.value == "")) {
//     if (password != repassword) {
//       alert("Passwords must be equal");
//     }
//   }
// });
