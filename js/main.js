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

let likeText;
document.addEventListener("click", (e) => {
    for (let item = 0; item < likeBtn.length; item++) {
        if (likeBtn[item] == e.target) {
            likeBtn[item].classList.toggle("fa-solid");
            likeBtn[item].classList.toggle("likeColor");
            if (likeBtn[item].classList.contains("fa-solid")) {
                const p = document.createElement('p');
                likeBtn[item].classList.add('countLike');
                p.innerHTML = `Liked by 1 users`;
                likeText = p;
                likeCount[item].appendChild(p)
            } else {
                likeCount[item].removeChild(likeText);
            }
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

document.addEventListener("click", (e) => {
    for (let item of commentBtn) {
        if (item == e.target) {
            location.href = "../comment.html"
        }
    }
});