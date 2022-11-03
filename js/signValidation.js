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

const toggleVisibilityOld = () => {
  let password = document.getElementById('oldpassword');
  let icon = document.getElementById('iconOld');
  passwordEye(password,icon)
}

const toggleVisibilitynew = () => {
  let password = document.getElementById('newpassword');
  let icon = document.getElementById('iconch');
  passwordEye(password,icon)
}
const toggleVisibilitynewRe = () => {
  let password = document.getElementById('newrepassword');
  let icon = document.getElementById('iconrech');
  passwordEye(password,icon)
}
