const dropdown = document.querySelector(".dropdown");
const dropdownIcon = document.querySelector("#dropdownIcon");
const burger = document.querySelector(".burger");
const burgerList = document.querySelector(".burgerList");
const line1 = document.querySelector(".line1");
const line2 = document.querySelector(".line2");
const line3 = document.querySelector(".line3");
const likeBtn = document.querySelectorAll(".like-icon");
const likeCount = document.querySelectorAll(".post-likes");
const commentBtn = document.querySelectorAll(".comment-icon");

burger.addEventListener("click", () => {
    line1.classList.toggle("linecross1");
    line2.classList.toggle("linecross2");
    line3.classList.toggle("linecross3");
    burgerList.classList.toggle("active");
    if (dropdown.classList.contains("active")) {
        dropdown.classList.remove("active");
        dropdownIcon.innerHTML = "arrow_drop_down";
    }
});

const dropdownOpen = () => {
    dropdown.classList.toggle("active");
    if (burgerList.classList.contains("active")) {
        line1.classList.remove("linecross1");
        line2.classList.remove("linecross2");
        line3.classList.remove("linecross3");
        burgerList.classList.remove("active");
    }
    if (dropdownIcon.innerHTML == "arrow_drop_up") {
        dropdownIcon.innerHTML = "arrow_drop_down";
    } else {
        dropdownIcon.innerHTML = "arrow_drop_up";
    }
};

const menusClose = () => {
    if (dropdown.classList.contains("active")) {
        dropdown.classList.remove("active");
        dropdownIcon.innerHTML = "arrow_drop_down";
    }
    if (burgerList.classList.contains("active")) {
        line1.classList.remove("linecross1");
        line2.classList.remove("linecross2");
        line3.classList.remove("linecross3");
        burgerList.classList.remove("active");
    }
};

document.addEventListener("click", (e) => {
    for (let item of likeBtn) {
        if (item == e.target) {
            item.classList.toggle("fa-solid");
            item.classList.toggle("likeColor");
        }
    }
});

document.addEventListener("click", (e) => {
    for (let item of commentBtn) {
        if (item == e.target) {
            location.href = "../comment.html"
        }
    }
});


