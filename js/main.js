const dropdown = document.querySelector(".dropdown");
const dropdownIcon = document.querySelector("#dropdownIcon");

const dropdownOpen = () => {
    dropdown.classList.toggle("active");
    if (dropdownIcon.innerHTML == "arrow_drop_up") {
        dropdownIcon.innerHTML = "arrow_drop_down";
    } else {
        dropdownIcon.innerHTML = "arrow_drop_up";
    }
};

const dropdownClose = () => {
    if (dropdown.classList.contains("active")) {
        dropdown.classList.remove("active");
        dropdownIcon.innerHTML = "arrow_drop_down";
    }
};

const burger = document.querySelector('.burger');
burger.addEventListener('click', () => {
    const burgerList = document.querySelector('.burgerList');
    const line1 = document.querySelector('.line1');
    const line2 = document.querySelector('.line2');
    const line3 = document.querySelector('.line3');
    line1.classList.toggle('linecross1');
    line2.classList.toggle('linecross2');
    line3.classList.toggle('linecross3');
    burgerList.classList.toggle('active');

})